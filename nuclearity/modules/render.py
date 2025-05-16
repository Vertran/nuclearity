import glfw
from data_exch import shared_data, normalize_color
from logger import make_log
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import json

def draw_rect(rect, color):
    center = [rect[2]/2, rect[3]/2]
    pos = [rect[0], rect[1]]

    color = normalize_color(color)

    if len(color) == 3:
        color.append(1.0)
    
    glColor4f(*color)

    glBegin(GL_QUADS)
    glVertex2f(pos[0] - center[0], pos[1] - center[1])
    glVertex2f(pos[0] + center[0], pos[1] - center[1])
    glVertex2f(pos[0] + center[0], pos[1] + center[1])
    glVertex2f(pos[0] - center[0], pos[1] + center[1])
    glEnd()

def main():

    if not glfw.init():
        return
    
    glutInit()
    window = glfw.create_window(*shared_data['screen'], "Cube Renderer", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    #glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    shared_data["window"] = window

    while not glfw.window_should_close(window) and shared_data["run"][0]:


        glClearColor(0.2, 0.2, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, shared_data["screen"][0], shared_data["screen"][1], 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        for element in shared_data["UI_elements"]:
            element.draw()

        glfw.swap_buffers(window)
        glfw.poll_events()


    shared_data["run"] = [False, [False, False]]
    glfw.terminate()

make_log("INFO", "RenderEngine started successfully")