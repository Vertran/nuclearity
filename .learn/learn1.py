import glfw
from OpenGL.GL import *

def main():
    if not glfw.init():
        raise RuntimeError('GLFW is not initialized')
    

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)


    window = glfw.create_window(800, 600, "my game", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError('Window is not created')

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
