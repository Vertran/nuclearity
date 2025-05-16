import render
import threading
import glfw
from data_exch import shared_data, Menu
from logger import make_log


def main():
    #screens.play("startup")
    shared_data["run"][1] = [False, True]
    
    while not shared_data["window"]:
        threading.Event().wait(0.1)

    window = shared_data["window"]

    Menu.load_menu("main_menu")
    while shared_data["run"][0]:
        
        mx, my = glfw.get_cursor_pos(window)

        for element in shared_data["UI_elements"]:
            element.update()
    make_log("INFO", "Main thread exited")




render_t = threading.Thread(target=render.main, name="RenderThread")
main_t = threading.Thread(target=main, name="MainThread")

main_t.start()
render_t.start()

render_t.join()
main_t.join()