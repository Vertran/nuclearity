import glfw
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

def draw_cube():
    vertices = [
        [1, 1, -1],
        [1, -1, -1],
        [-1, -1, -1],
        [-1, 1, -1],
        [1, 1, 1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, 1, 1]
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    faces = [
        (0, 1, 5, 4),  # Front face
        (1, 2, 6, 5),  # Right face
        (2, 3, 7, 6),  # Back face
        (3, 0, 4, 7),  # Left face
        (4, 5, 6, 7),  # Top face
        (0, 1, 2, 3)   # Bottom face
    ]

    glBegin(GL_LINES)
    glColor3f(0, 0, 0)
    for edge in edges:
        for vertex in edge:
            glColor3f(vertices[vertex][0] * 0.5, vertices[vertex][1] * 0.5, vertices[vertex][2] * 0.5)
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)
    for face in faces:
        for vertex in face:
            glColor3f(vertices[vertex][0], vertices[vertex][1], vertices[vertex][2])
            glVertex3fv(vertices[vertex])
    glEnd()

    def draw_sphere(radius=1.5, slices=32, stacks=32):
        glColor4f(1, 1, 1, 0)  # Set sphere color
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_LINE)  # Set sphere to wireframe mode
        gluSphere(quadric, radius, slices, stacks)
        #gluDeleteQuadric(quadric)
    draw_sphere()  # Draw sphere at the center of the cube

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Cube Renderer", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Set up camera
        gluPerspective(45, 800 / 600, 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        glRotatef(glfw.get_time() * 50, 1, 1, 1)

        draw_cube()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()