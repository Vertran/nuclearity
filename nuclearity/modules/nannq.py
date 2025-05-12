import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLUT import *
import numpy as np

# Window size
WIDTH, HEIGHT = 800, 600

# Vertex shader for fullscreen quad
VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec2 position;
layout (location = 1) in vec2 texCoords;

out vec2 TexCoords;

void main()
{
    TexCoords = texCoords;
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

# Fragment shader for horizontal blur
FRAG_SHADER_BLUR_HORIZONTAL = """
#version 330 core
in vec2 TexCoords;
out vec4 FragColor;

uniform sampler2D image;
uniform float texOffset; // 1.0 / texture width

void main()
{
    vec3 result = vec3(0.0);
    float weights[5] = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);

    for(int i = -4; i <= 4; ++i)
    {
        float weight = weights[abs(i)];
        vec2 offset = vec2(texOffset * i, 0.0);
        result += texture(image, TexCoords + offset).rgb * weight;
    }
    FragColor = vec4(result, 1.0);
}
"""

# Fragment shader for vertical blur
FRAG_SHADER_BLUR_VERTICAL = """
#version 330 core
in vec2 TexCoords;
out vec4 FragColor;

uniform sampler2D image;
uniform float texOffset; // 1.0 / texture height

void main()
{
    vec3 result = vec3(0.0);
    float weights[5] = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);

    for(int i = -4; i <= 4; ++i)
    {
        float weight = weights[abs(i)];
        vec2 offset = vec2(0.0, texOffset * i);
        result += texture(image, TexCoords + offset).rgb * weight;
    }
    FragColor = vec4(result, 1.0);
}
"""

# Simple vertex data for fullscreen quad
quad_vertices = np.array([
    # positions   # texCoords
    -1.0,  1.0,   0.0, 1.0,
    -1.0, -1.0,   0.0, 0.0,
     1.0, -1.0,   1.0, 0.0,

    -1.0,  1.0,   0.0, 1.0,
     1.0, -1.0,   1.0, 0.0,
     1.0,  1.0,   1.0, 1.0,
], dtype=np.float32)

def normalize_color(color):
    return [c / 255.0 for c in color]

def draw_text(pos, text, color=(255, 255, 255)):
    color = normalize_color(color)
    glColor3f(*color[:3])
    glRasterPos2f(pos[0], pos[1])
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def draw_rect(center_pos, size, color):
    color = normalize_color(color)
    if len(color) == 3:
        color.append(1.0)
    glColor4f(*color)
    cx, cy = center_pos
    w, h = size
    glBegin(GL_QUADS)
    glVertex2f(cx - w/2, cy - h/2)
    glVertex2f(cx + w/2, cy - h/2)
    glVertex2f(cx + w/2, cy + h/2)
    glVertex2f(cx - w/2, cy + h/2)
    glEnd()

def create_shader(vertex_src, fragment_src):
    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )
    return shader

def create_fbo(width, height):
    fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)

    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex, 0)

    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        raise RuntimeError("Framebuffer not complete")

    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    return fbo, tex

def main():
    if not glfw.init():
        return

    glutInit()

    window = glfw.create_window(WIDTH, HEIGHT, "Blur Behind UI Demo", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Setup OpenGL state
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Setup orthographic projection for 2D UI rendering
    glViewport(0, 0, WIDTH, HEIGHT)

    # Create FBOs for ping-pong blur
    fbo1, tex1 = create_fbo(WIDTH, HEIGHT)
    fbo2, tex2 = create_fbo(WIDTH, HEIGHT)

    # Compile shaders
    shader_blur_horizontal = create_shader(VERTEX_SHADER, FRAG_SHADER_BLUR_HORIZONTAL)
    shader_blur_vertical = create_shader(VERTEX_SHADER, FRAG_SHADER_BLUR_VERTICAL)

    # Setup VAO/VBO for fullscreen quad
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, quad_vertices.nbytes, quad_vertices, GL_STATIC_DRAW)

    # position attribute
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(0))
    # texCoords attribute
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(2 * quad_vertices.itemsize))

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # 1. Render background scene to fbo1
        glBindFramebuffer(GL_FRAMEBUFFER, fbo1)
        glViewport(0, 0, WIDTH, HEIGHT)
        glClearColor(0.1, 0.3, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw some simple colored rectangles as background
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        draw_rect((WIDTH/2, HEIGHT/2), (400, 300), (200, 100, 50, 255))
        draw_rect((WIDTH/2 + 100, HEIGHT/2 + 50), (200, 150), (50, 200, 100, 255))

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # 2. Apply horizontal blur: render fbo1 texture to fbo2 with horizontal blur shader
        glBindFramebuffer(GL_FRAMEBUFFER, fbo2)
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader_blur_horizontal)
        glUniform1f(glGetUniformLocation(shader_blur_horizontal, "texOffset"), 1.0 / WIDTH)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex1)
        glUniform1i(glGetUniformLocation(shader_blur_horizontal, "image"), 0)

        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)
        glUseProgram(0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # 3. Apply vertical blur: render fbo2 texture to default framebuffer with vertical blur shader
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(shader_blur_vertical)
        glUniform1f(glGetUniformLocation(shader_blur_vertical, "texOffset"), 1.0 / HEIGHT)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex2)
        glUniform1i(glGetUniformLocation(shader_blur_vertical, "image"), 0)

        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)
        glUseProgram(0)

        # 4. Draw UI elements on top (non-blurred)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Example UI: a semi-transparent rectangle and text
        draw_rect((WIDTH/2, HEIGHT/2), (300, 100), (50, 50, 50, 180))
        draw_text((WIDTH/2 - 60, HEIGHT/2 - 10), "Blurred Background", (255, 255, 255))
        draw_text((WIDTH/2 - 60, HEIGHT/2 + 10), "UI on top", (255, 255, 255))

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
