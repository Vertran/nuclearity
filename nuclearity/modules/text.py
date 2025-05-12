import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from random import randint

class Actives():
    def __init__(self, rect, color):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.hWidth = rect[2] / 2
        self.hHeight = rect[3] / 2
        self.color = [c/255.0 for c in color]

    def draw(self, win_pos):
        glBegin(GL_QUADS)
        glColor4f(*self.color, 0.5)
        glVertex2f(self.x - self.hWidth - win_pos[0], self.y - self.hHeight - win_pos[1])
        glVertex2f(self.x + self.hWidth - win_pos[0], self.y - self.hHeight - win_pos[1])
        glVertex2f(self.x + self.hWidth - win_pos[0], self.y + self.hHeight - win_pos[1])
        glVertex2f(self.x - self.hWidth - win_pos[0], self.y + self.hHeight - win_pos[1])
        glEnd()

def main():
    winWH = [800, 600]

    if not glfw.init():
        raise Exception("GLFW initialization failed")
    
    
    glfw.window_hint(glfw.DECORATED, glfw.FALSE)

    # Create the main window (hidden at the start)
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    main_window = glfw.create_window(800, 600, "Main Window", None, None)
    if not main_window:
        glfw.terminate()
        raise Exception("Failed to create main window")

    # Create win1
    win1 = glfw.create_window(*winWH, "Window 1", None, None)
    if not win1:
        glfw.terminate()
        raise Exception("Failed to create Window 1")

    # Create win2
    win2 = glfw.create_window(*winWH, "Window 2", None, None)
    if not win2:
        glfw.terminate()
        raise Exception("Failed to create Window 2")

    # Show the windows
    glfw.show_window(win1)
    glfw.show_window(win2)

    draw_win = [win1, win2]
    actives = []

    for _ in range(1920):
        color = [randint(50, 255) for _ in range(3)]
        rect = [randint(0, 1920), randint(0, 1080), 50, 50]
        actives.append(Actives(rect, color))
        print(f"Created rect: {rect} with color: {color}")

        # Set the viewport and projection for each window

    # Main loop
    while not glfw.window_should_close(win1) and not glfw.window_should_close(win2):
        # Calculate the distance between win1 and win2
        xpos1, ypos1 = glfw.get_window_pos(win1)
        xpos2, ypos2 = glfw.get_window_pos(win2)
        distance = ((xpos2 - xpos1) ** 2 + (ypos2 - ypos1) ** 2) ** 0.5

        if distance < 500:
            distance  /= 192
        distance = max(0, min(distance, 1))

        glfw.set_window_opacity(win1, distance)
        glfw.set_window_opacity(win2, distance)
        for window in draw_win:
            glfw.make_context_current(window)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            
            if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
                xpos, ypos = glfw.get_window_pos(win2)
                glfw.set_window_pos(win2, xpos, ypos - winWH[1] // 20)
            if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
                xpos, ypos = glfw.get_window_pos(win2)
                glfw.set_window_pos(win2, xpos, ypos + winWH[1] // 20)
            if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
                xpos, ypos = glfw.get_window_pos(win2)
                glfw.set_window_pos(win2, xpos - winWH[0] // 20, ypos)
            if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
                xpos, ypos = glfw.get_window_pos(win2)
                glfw.set_window_pos(win2, xpos + winWH[0] // 20, ypos)

            xpos, ypos = glfw.get_window_pos(window)
            width, height = glfw.get_window_size(window)

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(0, width, height, 0, -1, 1)  # координаты — левый верхний угол
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()


            # Calculate the center position
            #center_x = xpos + width // 2
            #center_y = ypos + height // 2

            # Set the window title to its center position
            #glfw.set_window_title(window, f"Center: ({center_x}, {center_y})")


            

            for active in actives:
                active.draw([xpos, ypos])


            glfw.swap_buffers(window)
        mx, my = glfw.get_cursor_pos(main_window)
        glfw.set_window_pos(win1, int(mx - width/2), int(my - height/2))

        glfw.poll_events()

    # Cleanup
    glfw.destroy_window(main_window)
    glfw.destroy_window(win1)
    glfw.destroy_window(win2)
    glfw.terminate()

if __name__ == "__main__":
    main()