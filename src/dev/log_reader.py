import glfw
import time
from OpenGL.GL import *

def main(path):
    if not glfw.init():
        return

    window = glfw.create_window(640, 480, "Log Reader 0.0.0", None, None)

    if not window:
        glfw.terminate()
        return


    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()

    for entry in data.split('\n['):
        pass

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):



        glfw.swap_buffers(window)
        glfw.poll_events()
        time.sleep(0.1)
    glfw.terminate()




if __name__ == '__main__':
    main(input('path?> '))