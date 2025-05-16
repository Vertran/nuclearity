import os
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Твой класс TEXT (замени на свою реализацию)
class TEXT:
    def __init__(self, pos, color, size, text):
        self.x, self.y = pos
        self.color = color
        self.size = size
        self.text = text

    def draw(self):
        glColor3f(*self.color)
        glRasterPos2f(self.x, self.y)
        for char in self.text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

# Класс папки в виде квадрата
class FolderSquare:
    def __init__(self, x, y, size, name):
        self.x = x
        self.y = y
        self.size = size
        self.name = name
        self.text = TEXT((x + 5, y + size / 2 - 5), (1, 1, 1), 0.5, name)

    def draw(self):
        glColor3f(0.2, 0.4, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.size, self.y)
        glVertex2f(self.x + self.size, self.y + self.size)
        glVertex2f(self.x, self.y + self.size)
        glEnd()
        self.text.draw()

    def is_inside(self, mx, my):
        return self.x <= mx <= self.x + self.size and self.y <= my <= self.y + self.size
    
class DropdownMenu:
    def __init__(self, x, y, width, options, callback):
        self.x = x
        self.y = y
        self.width = width
        self.options = options
        self.callback = callback
        self.open = False
        self.height = 25
        self.selected = options[0] if options else ""
        self.hover_index = -1

    def draw(self):
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()
        text = TEXT((self.x + 5, self.y + 7), (1, 1, 1), 1, self.selected)
        text.draw()

        if self.open:
            for i, option in enumerate(self.options):
                if i == self.hover_index:
                    glColor3f(0.2, 0.5, 0.8)
                else:
                    glColor3f(0.2, 0.2, 0.2)
                glBegin(GL_QUADS)
                glVertex2f(self.x, self.y + (i+1)*self.height)
                glVertex2f(self.x + self.width, self.y + (i+1)*self.height)
                glVertex2f(self.x + self.width, self.y + (i+2)*self.height)
                glVertex2f(self.x, self.y + (i+2)*self.height)
                glEnd()
                t = TEXT((self.x + 5, self.y + (i+1)*self.height + 7), (1, 1, 1), 1, option)
                t.draw()

    def is_inside(self, mx, my):
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height

    def click(self, mx, my):
        if self.open:
            index = int((my - self.y) / self.height) - 1
            if 0 <= index < len(self.options):
                self.selected = self.options[index]
                self.callback(self.selected)
            self.open = False
        else:
            self.open = True

    def hover(self, mx, my):
        if self.open:
            index = int((my - self.y) / self.height) - 1
            self.hover_index = index if 0 <= index < len(self.options) else -1


# Настройка окна
WIDTH, HEIGHT = 800, 600
if not glfw.init():
    raise Exception("glfw init failed")

window = glfw.create_window(WIDTH, HEIGHT, "Mini Explorer", None, None)
if not window:
    glfw.terminate()
    raise Exception("glfw window failed")

glfw.make_context_current(window)
glutInit()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)
glMatrixMode(GL_MODELVIEW)


current_path = os.getcwd()
folders = []

def build_folders(path):
    global folders
    folders = []
    size = 100
    gap = 20
    x, y = 10, 10

    # Если не корень — добавляем ".." (вверх)
    if os.path.dirname(path) != path:
        folders.append(FolderSquare(x, y, size, ".."))
        x += size + gap

    try:
        for folder in os.listdir(path):
            full = os.path.join(path, folder)
            if os.path.isdir(full):
                folders.append(FolderSquare(x, y, size, folder))
                x += size + gap
                if x + size > WIDTH:
                    x = 10
                    y += size + gap
    except PermissionError:
        pass


def on_mouse_button(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        mx, my = glfw.get_cursor_pos(window)
        menu.click(mx, my)
        glfw.poll_events()
        for folder in folders:
            if folder.is_inside(mx, my):
                global current_path
                if folder.name == "..":
                    current_path = os.path.dirname(current_path)
                else:
                    current_path = os.path.join(current_path, folder.name)
                build_folders(current_path)
                break


def change_path(new_path):
    global current_path
    current_path = new_path
    build_folders(current_path)


disks = [d + ":\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(d + ":\\")]
menu = DropdownMenu(10, 10, 150, disks, lambda sel: change_path(sel))

glfw.set_mouse_button_callback(window, on_mouse_button)
build_folders(current_path)

# Главный цикл
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    for folder in folders:
        folder.draw()

    menu.draw()


    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
