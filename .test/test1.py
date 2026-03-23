"""
Multiplicative feedback shader demo.
Квадрат в 3D сцене, ping-pong FBO, feedback = prev * curr (по яркости).

Управление:
  WASD      — вращение квадрата
  R         — сброс
  +/-       — изменить decay множитель
  ESC       — выход
"""

import ctypes
import math
import sys

import glfw
import numpy as np
from OpenGL.GL import *

# ─────────────────────────────────────────────────────────────
#  ШЕЙДЕРЫ
# ─────────────────────────────────────────────────────────────

SCENE_VERT = """
#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;

uniform mat4 uMVP;

out vec3 vColor;

void main() {
    gl_Position = uMVP * vec4(aPos, 1.0);
    vColor = aColor;
}
"""

SCENE_FRAG = """
#version 330 core
in vec3 vColor;
out vec4 FragColor;

void main() {
    FragColor = vec4(vColor, 1.0);
}
"""

# Feedback: берём prev (ч/б яркость) * curr (яркость) → результат
FEEDBACK_VERT = """
#version 330 core
layout(location = 0) in vec2 aPos;
layout(location = 1) in vec2 aUV;
out vec2 vUV;
void main() {
    gl_Position = vec4(aPos, 0.0, 1.0);
    vUV = aUV;
}
"""

FEEDBACK_FRAG = """
#version 330 core
in vec2 vUV;
out vec4 FragColor;

uniform sampler2D uCurrent;   // текущая сцена
uniform sampler2D uPrev;      // прошлый feedback
uniform float uDecay;         // множитель затухания (0..1)

float luminance(vec3 c) {
    return dot(c, vec3(0.2126, 0.7152, 0.0722));
}
void main() {
    vec3 curr     = texture(uCurrent, vUV).rgb;
    vec3 prev     = texture(uPrev,    vUV).rgb;

    float lCurr = luminance(curr);
    float lPrev = luminance(prev) * uDecay;

    float merged = clamp(lPrev + lCurr, 0.0, 1.0);

    // Цвет: где объект есть — берём его цвет,
    // где только след — берём цвет из prev (он уже накопил нужный цвет)
    vec3 color = lCurr > 0.01 ? curr : prev;

    FragColor = vec4(color * merged, 1.0);
}
"""

# Финальный blit на экран (просто сэмплер)
BLIT_FRAG = """
#version 330 core
in vec2 vUV;
out vec4 FragColor;
uniform sampler2D uTex;
void main() {
    FragColor = texture(uTex, vUV);
}
"""

# ─────────────────────────────────────────────────────────────
#  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ─────────────────────────────────────────────────────────────

def compile_shader(src, kind):
    s = glCreateShader(kind)
    glShaderSource(s, src)
    glCompileShader(s)
    if not glGetShaderiv(s, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(s).decode())
    return s

def link_program(*shaders):
    prog = glCreateProgram()
    for s in shaders: glAttachShader(prog, s)
    glLinkProgram(prog)
    if not glGetProgramiv(prog, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(prog).decode())
    for s in shaders: glDeleteShader(s)
    return prog

def make_fbo(w, h):
    fbo = glGenFramebuffers(1)
    tex = glGenTextures(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB16F, w, h, 0, GL_RGB, GL_FLOAT, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex, 0)

    # depth renderbuffer — нужен для 3D сцены
    rbo = glGenRenderbuffers(1)
    glBindRenderbuffer(GL_RENDERBUFFER, rbo)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, w, h)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, rbo)

    status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
    if status != GL_FRAMEBUFFER_COMPLETE:
        raise RuntimeError(f"FBO incomplete: {status}")
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    return fbo, tex

# ─────────────────────────────────────────────────────────────
#  МАТРИЦЫ (без numpy линалг зависимостей, чисто руками)
# ─────────────────────────────────────────────────────────────

def mat4_identity():
    return np.eye(4, dtype=np.float32)

def mat4_rotate_x(a):
    c, s = math.cos(a), math.sin(a)
    m = np.eye(4, dtype=np.float32)
    m[1,1] = c;  m[1,2] = -s
    m[2,1] = s;  m[2,2] =  c
    return m

def mat4_rotate_y(a):
    c, s = math.cos(a), math.sin(a)
    m = np.eye(4, dtype=np.float32)
    m[0,0] = c;  m[0,2] =  s
    m[2,0] =-s;  m[2,2] =  c
    return m

def mat4_perspective(fovy, aspect, near, far):
    f = 1.0 / math.tan(fovy / 2)
    m = np.zeros((4,4), dtype=np.float32)
    m[0,0] = f / aspect
    m[1,1] = f
    m[2,2] = (far + near) / (near - far)
    m[2,3] = (2 * far * near) / (near - far)
    m[3,2] = -1.0
    return m

def mat4_translate(x, y, z):
    m = np.eye(4, dtype=np.float32)
    m[0,3] = x; m[1,3] = y; m[2,3] = z
    return m

# ─────────────────────────────────────────────────────────────
#  ГЕОМЕТРИЯ
# ─────────────────────────────────────────────────────────────

def make_quad_vao():
    # Квадрат с разными цветами по вершинам: pos(3) + color(3)
    verts = np.array([
        -0.5, -0.5, 0.0,   1.0, 0.2, 0.1,
         0.5, -0.5, 0.0,   0.1, 1.0, 0.3,
         0.5,  0.5, 0.0,   0.2, 0.4, 1.0,
        -0.5,  0.5, 0.0,   1.0, 0.9, 0.1,
    ], dtype=np.float32)
    idxs = np.array([0,1,2, 0,2,3], dtype=np.uint32)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, verts.nbytes, verts, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, idxs.nbytes, idxs, GL_STATIC_DRAW)
    stride = 6 * 4
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)
    return vao

def make_screen_quad_vao():
    # Fullscreen quad для постпроцессинга: pos(2) + uv(2)
    verts = np.array([
        -1,-1,  0,0,
         1,-1,  1,0,
         1, 1,  1,1,
        -1, 1,  0,1,
    ], dtype=np.float32)
    idxs = np.array([0,1,2, 0,2,3], dtype=np.uint32)
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, verts.nbytes, verts, GL_STATIC_DRAW)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, idxs.nbytes, idxs, GL_STATIC_DRAW)
    stride = 4 * 4
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(8))
    glEnableVertexAttribArray(1)
    glBindVertexArray(0)
    return vao

# ─────────────────────────────────────────────────────────────
#  ГЛАВНЫЙ КЛАСС
# ─────────────────────────────────────────────────────────────

class App:
    W, H = 900, 600

    def __init__(self):
        if not glfw.init():
            raise RuntimeError("GLFW init failed")
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self.win = glfw.create_window(self.W, self.H, "Multiplicative Feedback", None, None)
        glfw.make_context_current(self.win)
        glfw.set_key_callback(self.win, self.on_key)

        # Состояние
        self.rot_x = 0.3
        self.rot_y = 0.4
        self.decay = 1.1   # ключевой параметр! 0.9 = быстрое затухание, 0.999 = долгий след
        self.keys  = set()  # зажатые клавиши
        self.vel_x = 0.0
        self.vel_y = 0.0

        self._build_gl()

    def _build_gl(self):
        # Программы
        self.prog_scene    = link_program(
            compile_shader(SCENE_VERT,    GL_VERTEX_SHADER),
            compile_shader(SCENE_FRAG,    GL_FRAGMENT_SHADER))
        self.prog_feedback = link_program(
            compile_shader(FEEDBACK_VERT, GL_VERTEX_SHADER),
            compile_shader(FEEDBACK_FRAG, GL_FRAGMENT_SHADER))
        self.prog_blit     = link_program(
            compile_shader(FEEDBACK_VERT, GL_VERTEX_SHADER),
            compile_shader(BLIT_FRAG,     GL_FRAGMENT_SHADER))

        # Геометрия
        self.quad_vao   = make_quad_vao()
        self.screen_vao = make_screen_quad_vao()

        # FBO: A — сцена, B и C — ping-pong feedback
        self.fbo_scene, self.tex_scene = make_fbo(self.W, self.H)
        self.fbo_ping,  self.tex_ping  = make_fbo(self.W, self.H)
        self.fbo_pong,  self.tex_pong  = make_fbo(self.W, self.H)

        # Очищаем оба feedback FBO
        for fbo in (self.fbo_ping, self.fbo_pong):
            glBindFramebuffer(GL_FRAMEBUFFER, fbo)
            glClearColor(0,0,0,1)
            glClear(GL_COLOR_BUFFER_BIT)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        self.frame = 0

    def on_key(self, win, key, sc, action, mods):
        if action == glfw.PRESS:
            self.keys.add(key)
            if key == glfw.KEY_R:
                self.rot_x = 0.3; self.rot_y = 0.4
                for fbo in (self.fbo_ping, self.fbo_pong):
                    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
                    glClear(GL_COLOR_BUFFER_BIT)
                glBindFramebuffer(GL_FRAMEBUFFER, 0)
            if key == glfw.KEY_EQUAL: self.decay = min(2, self.decay + 0.05)
            if key == glfw.KEY_MINUS: self.decay = max(0.7,   self.decay - 0.05)
            if key == glfw.KEY_ESCAPE: glfw.set_window_should_close(win, True)
        elif action == glfw.RELEASE:
            self.keys.discard(key)

    def process_keys(self):
        accel   = 0.02   # разгон
        friction = 0.95   # торможение (0..1, чем меньше — тем быстрее тормозит)
        max_vel = 1    # ограничение скорости

        if glfw.KEY_W in self.keys: self.vel_x -= accel
        if glfw.KEY_S in self.keys: self.vel_x += accel
        if glfw.KEY_A in self.keys: self.vel_y -= accel
        if glfw.KEY_D in self.keys: self.vel_y += accel

        # Трение применяется всегда — и при зажатой кнопке, и без
        self.vel_x *= friction
        self.vel_y *= friction

        # Clamp
        self.vel_x = max(-max_vel, min(max_vel, self.vel_x))
        self.vel_y = max(-max_vel, min(max_vel, self.vel_y))

        self.rot_x += self.vel_x
        self.rot_y += self.vel_y

    def draw_scene_to_fbo(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo_scene)
        glViewport(0, 0, self.W, self.H)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        proj  = mat4_perspective(math.radians(60), self.W/self.H, 0.1, 100.0)
        view  = mat4_translate(0, 0, -2.0)
        model = mat4_rotate_x(self.rot_x) @ mat4_rotate_y(self.rot_y)
        mvp   = proj @ view @ model

        glUseProgram(self.prog_scene)
        glUniformMatrix4fv(
            glGetUniformLocation(self.prog_scene, "uMVP"),
            1, GL_TRUE, mvp)
        glBindVertexArray(self.quad_vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        glDisable(GL_DEPTH_TEST)

    def apply_feedback(self, tex_prev):
        # Пишем в текущий "pong", читаем из prev
        fbo_write = self.fbo_pong if (self.frame % 2 == 0) else self.fbo_ping
        glBindFramebuffer(GL_FRAMEBUFFER, fbo_write)
        glViewport(0, 0, self.W, self.H)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.prog_feedback)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_scene)
        glUniform1i(glGetUniformLocation(self.prog_feedback, "uCurrent"), 0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, tex_prev)
        glUniform1i(glGetUniformLocation(self.prog_feedback, "uPrev"), 1)
        glUniform1f(glGetUniformLocation(self.prog_feedback, "uDecay"), self.decay)

        glBindVertexArray(self.screen_vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        return fbo_write, (self.tex_pong if (self.frame % 2 == 0) else self.tex_ping)

    def blit_to_screen(self, tex):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, self.W, self.H)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.prog_blit)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex)
        glUniform1i(glGetUniformLocation(self.prog_blit, "uTex"), 0)

        glBindVertexArray(self.screen_vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def run(self):
        print("Управление:")
        print("  WASD   — вращение квадрата")
        print("  R      — сброс")
        print("  +/-    — decay множитель (сейчас {:.3f})".format(self.decay))
        print("  ESC    — выход")

        while not glfw.window_should_close(self.win):
            glfw.poll_events()
            self.process_keys()

            # Какой буфер "прошлый" на этом кадре
            tex_prev = self.tex_ping if (self.frame % 2 == 0) else self.tex_pong

            # 1. Рисуем 3D сцену в отдельный FBO
            self.draw_scene_to_fbo()

            # 2. Применяем multiplicative feedback
            _, tex_result = self.apply_feedback(tex_prev)

            # 3. Blit результата на экран
            self.blit_to_screen(tex_result)

            title = f"Multiplicative Feedback  |  decay={self.decay:.3f}  |  WASD вращение  R сброс  +/- decay"
            glfw.set_window_title(self.win, title)

            glfw.swap_buffers(self.win)
            self.frame += 1

        glfw.terminate()

if __name__ == "__main__":
    App().run()