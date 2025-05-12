import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

quad = None  # Для накопления предыдущего кадра (motion blur)


def main():
    global quad
    if not glfw.init():
        return

    window = glfw.create_window(640, 480, "LOBOTOMY", None, None)
    glfw.set_window_pos(window, 500, 400)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Используем accumulation buffer
    glClearAccum(0.0, 0.0, 0.0, 0.0)

    def draw_cube(x, y, z, size):
        half = size / 2
        glBegin(GL_QUADS)

        # Front face
        glVertex3f(x - half, y - half, z + half)
        glVertex3f(x + half, y - half, z + half)
        glVertex3f(x + half, y + half, z + half)
        glVertex3f(x - half, y + half, z + half)

        # Back face
        glVertex3f(x - half, y - half, z - half)
        glVertex3f(x - half, y + half, z - half)
        glVertex3f(x + half, y + half, z - half)
        glVertex3f(x + half, y - half, z - half)

        # Top
        glVertex3f(x - half, y + half, z - half)
        glVertex3f(x - half, y + half, z + half)
        glVertex3f(x + half, y + half, z + half)
        glVertex3f(x + half, y + half, z - half)

        # Bottom
        glVertex3f(x - half, y - half, z - half)
        glVertex3f(x + half, y - half, z - half)
        glVertex3f(x + half, y - half, z + half)
        glVertex3f(x - half, y - half, z + half)

        # Right
        glVertex3f(x + half, y - half, z - half)
        glVertex3f(x + half, y + half, z - half)
        glVertex3f(x + half, y + half, z + half)
        glVertex3f(x + half, y - half, z + half)

        # Left
        glVertex3f(x - half, y - half, z - half)
        glVertex3f(x - half, y - half, z + half)
        glVertex3f(x - half, y + half, z + half)
        glVertex3f(x - half, y + half, z - half)

        glEnd()

    cam_pos = [0.0, 0.0, 5.0]
    cam_yaw = 0.0
    speed = 0.001
    y_speed = 0.0
    cam_yaw_speed = 0.0
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_cube(0, 0, 0, 2)
    glAccum(GL_LOAD, 1.0)


    while not glfw.window_should_close(window):
        glEnable(GL_DEPTH_TEST)
        #glColor4f(1.0, 1.0, 1.0, 0.99)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, 640 / 480, 0.1, 100.0)

        cam_front = [
            math.sin(math.radians(cam_yaw)),
            0.0,
            -math.cos(math.radians(cam_yaw))
        ]
        cam_target = [
            cam_pos[0] + cam_front[0],
            cam_pos[1] + cam_front[1],
            cam_pos[2] + cam_front[2]
        ]

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(*cam_pos, *cam_target, 0.0, 1.0, 0.0)

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            cam_pos[0] += cam_front[0] * speed
            cam_pos[2] += cam_front[2] * speed
            speed += round((0.2 - speed) * 0.1, 2)
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            cam_pos[0] += cam_front[0] * speed
            cam_pos[2] += cam_front[2] * speed
            speed += round((-0.2 - speed) * 0.1, 2)
        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS and cam_pos[1] <= 0.1:
            y_speed += 0.5
        if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
            cam_yaw_speed += (-1 - cam_yaw_speed) * 0.001
        if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS:
            cam_yaw_speed += (1 - cam_yaw_speed) * 0.001

        cam_yaw_speed = round(cam_yaw_speed, 5)
        cam_yaw += cam_yaw_speed
        cam_yaw_speed += (0 - cam_yaw_speed) * 0.01

        cam_pos[1] += y_speed

        if cam_pos[1] > 0.1:
            y_speed -= 0.005
        else:
            y_speed = 0

        # Затухаем старый кадр (умножаем буфер накопления на коэффициент)
        glAccum(GL_MULT, 0.9)

        # Очищаем буфер цвета и глубины
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Рисуем сцену
        draw_cube(0, 0, 0, 2)

        # Добавляем новый кадр в буфер накопления
        glAccum(GL_ACCUM, 0.1)

        # Возвращаем итоговое изображение на экран
        glAccum(GL_RETURN, 1.0)


        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
