import modules.instancer as instancer
assert instancer.log is not None
log = instancer.log

from OpenGL.GL import * #type: ignore
import numpy as np
import glfw



class VideoManager:
    def __init__(self):
        #==> imports
        import ctypes

        #==> base
        log.info("Initializing Video Manager")
        self.screen = None
        self.clock = None
        if not glfw.init():
            log.error('GLFW is not inited')

        #==> glfw
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        #==> window
        self.window = None

        self.create_window()
        self.init_vert()

        #==> buffers
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW) #type: ignore

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glBindVertexArray(0)


        self.shader_program = self.create_program('data/shaders/', 'vertex.glsl', 'fragment.glsl')

        #==> post
        instancer.managers["video"] = self
        log.info("Video Manager initialized successfully")


    def create_program(self, folder_path, vert_shader, frag_shader):
        def compile_shader(source, shader_type):
            shader = glCreateShader(shader_type)
            glShaderSource(shader, source)
            glCompileShader(shader)

            if not glGetShaderiv(shader, GL_COMPILE_STATUS):
                error = glGetShaderInfoLog(shader).decode()
                log.error('Shader Compilation Error:', error)
                raise RuntimeError(f"Shader Compilation Error: {error}")

            return shader


        with open(folder_path+vert_shader, 'r', encoding='utf-8') as f:
            VERTEX_SHADER = f.read()


        with open(folder_path+frag_shader, 'r', encoding='utf-8') as f:
            FRAGMENT_SHADER = f.read()

        if not VERTEX_SHADER:
            log.warn('No Vertex shader found. Fallback to default')
            VERTEX_SHADER = """
#version 330 core

layout(location = 0) in vec3 aPos;

void main() {
    gl_Position = vec4(aPos, 1.0);
}
"""

        if not FRAGMENT_SHADER:
            log.warn('No Fragment shader found. Fallback to default')
            FRAGMENT_SHADER = """
#version 330 core

out vec4 FragColor;

void main() {
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);
}
"""

        vert = compile_shader(VERTEX_SHADER, GL_VERTEX_SHADER)
        frag = compile_shader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

        self.program = glCreateProgram()
        glAttachShader(self.program, vert)
        glAttachShader(self.program, frag)
        glLinkProgram(self.program)

        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(self.program).decode()
            log.error('Linking Programm error:', error)
            raise RuntimeError(f"Linking programm error: {error}")

        
        glDeleteShader(vert)
        glDeleteShader(frag)

        return self.program


    def init_vert(self, vertices=None):
        if vertices is not None:
            self.vertices = vertices
        else:
            log.warn('No vertiсes provided', 'Filling with basic triangle')
            self.vertices = np.array([
                -0.5, -0.5, 0.0,
                0.5, -0.5, 0.0,
                0.0,  0.5, 0.0,
            ], dtype=np.float32)

        
    def create_window(self, dimensions=[800, 600], name="No Name Provided jerk"):
        w = dimensions[0]
        h = dimensions[1]
        self.window = glfw.create_window(w, h, name, None, None)

        glfw.make_context_current(self.window)

    def main(self):
        #==> CLEAR ON CLOSE
        if glfw.window_should_close(self.window):
            glDeleteVertexArrays(1, [self.VAO])
            glDeleteBuffers(1, [self.VBO])
            glDeleteProgram(self.shader_program)
            glfw.terminate()

            return


        glfw.poll_events()

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(self.shader_program)
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(self.window)

        