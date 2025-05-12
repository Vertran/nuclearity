import render
import threading
import screens
from data_exch import *
from logger import make_log


def main():
    #screens.play("startup")
    shared_data["run"][1] = [False, True]

    Menu.load_menu("settings")
    while shared_data["run"][0]:
        threading.Event().wait(0.1)
    make_log("INFO", "Main thread exited")




render_t = threading.Thread(target=render.main, name="RenderThread")
main_t = threading.Thread(target=main, name="MainThread")

main_t.start()
render_t.start()

render_t.join()
main_t.join()