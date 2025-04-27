import glfw
from data_exch import *
from logger import make_log
from objects import Filler, Button, Label, ScrollField

def in_menus():
    return shared_data["menu"] in ['main_menu', 'settings']

def main():

    if not glfw.init():
        make_log("ERROR", "GLFW initialization failed")
        return

    window = glfw.create_window(*shared_data["screen"], "NUCLEARITY")
    glfw.make_context_current(window)
    if not window:
        make_log("ERROR", "Window creation failed")
        glfw.terminate()
        return
    
    while shared_data["run"][0]:
        if shared_data["run"][1]:
            glfw.poll_events()
            glfw.swap_buffers(window)

make_log("INFO", "RenderEngine started successfully")