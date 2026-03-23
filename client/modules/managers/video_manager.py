import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log

assert instancer.managers["object"] is not None
object_manager = instancer.managers["object"]

import ctypes
import os

import glfw
import glm
import numpy as np
import yaml
from OpenGL.GL import *


class VideoManager:
    def __init__(self):

        # ==> base
        log.info("Initializing Video Manager")
        self.screen = None
        self.clock = None

        # os.environ["XDG_SESSION_TYPE"] = "wayland"
        if not glfw.init():  # glfw.init_hint(glfw.PLATFORM, glfw.PLATFORM_WAYLAND):
            log.error("GLFW is not initialised")

        # ==> glfw
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # ==> window
        self.window = None

        with open("client/data/styles/window.yaml", "r", encoding="utf-8") as f:
            window_config = yaml.safe_load(f)["game"][0]

        self.create_window(**window_config)
        if not self.window:
            log.error("Failed to create GLFW window")
            glfw.terminate()
            raise RuntimeError("GLFW window creation failed")

        self.view = glm.lookAt(
            glm.vec3(0, 0, 10),
            glm.vec3(0, 0, 0),
            glm.vec3(0, 1, 0)
        )

        self.draw_objects = []
        self.update_objects = []

        object_manager.create_from_file("client/data/styles/main_menu/menu.yaml")
        self.clone_buffers()

        #        self.init_vert()

        # ==> buffers
        #        self.VAO = glGenVertexArrays(1)
        #        self.VBO = glGenBuffers(1)

        #        glBindVertexArray(self.VAO)

        #        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        #        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW) #type: ignore

        #        stride = 4 * 4
        #        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        #        glEnableVertexAttribArray(0)
        #        glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        #        glEnableVertexAttribArray(1)
        #        glBindVertexArray(0)

        self.shader_program = self.create_program("client/data/shaders/", "ui.vert.glsl", "ui.frag.glsl")

        # ==> post
        instancer.managers["video"] = self
        log.info("Video Manager initialized successfully")

    def create_program(self, folder_path, vert_shader, frag_shader):
        def compile_shader(source, shader_type):
            shader = glCreateShader(shader_type)
            glShaderSource(shader, source)
            glCompileShader(shader)

            if not glGetShaderiv(shader, GL_COMPILE_STATUS):
                error = glGetShaderInfoLog(shader).decode()
                log.error("Shader Compilation Error:", error)
                raise RuntimeError(f"Shader Compilation Error: {error}")

            return shader

        with open(folder_path + vert_shader, "r", encoding="utf-8") as f:
            VERTEX_SHADER = f.read()

        with open(folder_path + frag_shader, "r", encoding="utf-8") as f:
            FRAGMENT_SHADER = f.read()

        if not VERTEX_SHADER:
            log.warn("No Vertex shader found. Fallback to default")
            VERTEX_SHADER = """
            #version 330 core

            layout(location = 0) in vec3 aPos;
            layout(location = 1) in vec3 aColor;

            out vec3 vertexColor;

            void main() {
                gl_Position = vec4(aPos, 1.0);
                vertexColor = aColor;
            }
            """

        if not FRAGMENT_SHADER:
            log.warn("No Fragment shader found. Fallback to default")
            FRAGMENT_SHADER = """
            #version 330 core

            in vec3 vertexColor;
            out vec4 FragColor;

            void main() {
                FragColor = vec4(vertexColor, 1.0);
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
            log.error("Linking Programm error:", error)
            raise RuntimeError(f"Linking programm error: {error}")

        glDeleteShader(vert)
        glDeleteShader(frag)

        return self.program

    def get_program(self):
        return self.program

    def init_vert(self, vertices=None):
        if vertices is not None:
            self.vertices = vertices
        else:
            log.warn("No vertiсes provided", "Filling with basic triangle")
            self.vertices = np.array(
                [ # fmt: off
                    -0.5, -0.5,  0.0,
                     1.0,  0.0,  0.0,
                     0.5, -0.5,  0.0,
                     0.0,  1.0,  0.0,
                     0.0,  0.5,  0.0,
                     0.0,  0.0,  1.0,
                ], # fmt: on
                dtype=np.float32,
            )

    def create_window(self, **conf):
        dim = conf.get("resolution", "1920x1080").split("x")
        w = int(dim[0])
        h = int(dim[1])

        name = conf.get("title", "No Name Provided Jerk")

        if conf.get("fullscreen", False):
            monitor = glfw.get_primary_monitor()
        else:
            monitor = None

        self.window = glfw.create_window(w, h, name, monitor, None)

        glfw.make_context_current(self.window)

        w, h = glfw.get_framebuffer_size(self.window)
        self.projection = glm.perspective(glm.radians(45.0), w/h, 0.1, 1000.0)

        glViewport(0, 0, w, h)

        fw, fh = glfw.get_framebuffer_size(self.window)
        glViewport(0, 0, fw, fh)

        def on_resize(window, rw, rh):
            glViewport(0, 0, rw, rh)
            self.projection = glm.perspective(glm.radians(45.0), w/h, 0.1, 1000.0)

        glfw.set_framebuffer_size_callback(self.window, on_resize)

        instancer.screen["dim"] = [w, h]
        instancer.screen["fdim"] = [fw, fh]
        instancer.screen["name"] = name

        log.info(f"Created window: `{name}` [{w}x{h}] framebuffer:[{fw}x{fh}]")

    def clone_buffers(self):
        obj = object_manager.get_objects()
        self.draw_objects = obj[0]
        self.update_objects = obj[1]
        log.info("Cloned buffers")

    def main(self):
        glUseProgram(self.shader_program)
        glUniform1i(glGetUniformLocation(self.shader_program, "uTexture"), 0)

        locs = {
            "proj":         glGetUniformLocation(self.shader_program, "uProjection"),
            "base":         glGetUniformLocation(self.shader_program, "uBaseCol"),
            "out":          glGetUniformLocation(self.shader_program, "uOutCol"),
            "hBase":        glGetUniformLocation(self.shader_program, "uHoverBaseCol"),
            "hOut":         glGetUniformLocation(self.shader_program, "uHoverOutCol"),
            "state":        glGetUniformLocation(self.shader_program, "uHoverState"),
            "use_texture":  glGetUniformLocation(self.shader_program, "uUseTexture"),
            "view":         glGetUniformLocation(self.shader_program, "uView"),
            "model":        glGetUniformLocation(self.shader_program, "uModel"),
        }
        while instancer.state["drawing"]:
            # ==> CLEAR ON CLOSE
            if glfw.window_should_close(self.window):
                log.info("Window closed. Terminating")

                for object in self.draw_objects:
                    glDeleteVertexArrays(1, [object.VAO])
                    glDeleteBuffers(1, [object.VBO])

                glDeleteProgram(self.shader_program)
                glfw.terminate()

                return

            glfw.poll_events()
            glClearColor(0.1, 0.1, 0.1, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader_program)
            glUniformMatrix4fv(locs["proj"], 1, GL_FALSE, glm.value_ptr(self.projection))

            mouse_x, mouse_y = glfw.get_cursor_pos(self.window)

            glUniformMatrix4fv(locs["view"], 1, GL_FALSE, glm.value_ptr(self.view))

            for object in self.update_objects:
                object.update(cur_pos=(mouse_x, mouse_y))

            for object in self.draw_objects:
                uniforms = object.get_uniforms()

                glUniform1i(locs["use_texture"], uniforms["use_texture"])
                glUniform1f(locs["state"], uniforms["state"])
                glUniform3f(locs["base"], *uniforms["base"])
                glUniform3f(locs["out"], *uniforms["out"])
                glUniform3f(locs["hBase"], *uniforms["hBase"])
                glUniform3f(locs["hOut"], *uniforms["hOut"])
                glUniformMatrix4fv(locs["model"], 1, GL_FALSE, glm.value_ptr(uniforms["model"]))
                object.draw()

            glfw.swap_buffers(self.window)
