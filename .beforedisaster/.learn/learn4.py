import glfw
from OpenGL.GL import *
import numpy as np
import ctypes
import math

VERTEX_SHADER = """
#version 330 core

layout(location = 0) in vec3 aPos;

void main() {
    gl_Position = vec4(aPos, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330 core

uniform vec4 uColor;  // uniform — приходит из Python, одинаков для всего треугольника
out vec4 FragColor;

void main() {
    FragColor = uColor;
}
"""

vertices = np.array([
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0,
     0.0,  0.5, 0.0,
], dtype=np.float32)


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader).decode())
    return shader

def create_program(vert_src, frag_src):
    vert = compile_shader(vert_src, GL_VERTEX_SHADER)
    frag = compile_shader(frag_src, GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vert)
    glAttachShader(program, frag)
    glLinkProgram(program)
    glDeleteShader(vert)
    glDeleteShader(frag)
    return program


def main():
    if not glfw.init():
        raise RuntimeError()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "Uniform", None, None)
    glfw.make_context_current(window)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glBindVertexArray(0)

    shader = create_program(VERTEX_SHADER, FRAGMENT_SHADER)

    # Узнаём где в шейдере живёт uColor — получаем его "адрес"
    color_location = glGetUniformLocation(shader, "uColor")

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Время с запуска программы
        t = glfw.get_time()

        # Считаем цвет через синус — плавно колышется от 0 до 1
        r = math.sin(t) * 0.5 + 0.5
        g = math.sin(t + 2.0) * 0.5 + 0.5
        b = math.sin(t + 4.0) * 0.5 + 0.5

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader)

        # Передаём цвет в шейдер
        glUniform4f(color_location, r, g, b, 1.0)

        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()