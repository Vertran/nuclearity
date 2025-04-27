import pygame, render, threading, time, screens
from data_exch import shared_data, load_menu, Button, Label
from logger import make_log

pygame.init()
"""
screen = pygame.display.set_mode(shared_data["screen"][:2], shared_data["screen"][2])
pygame.display.set_caption("NUCLEARITY")
shared_data["window"] = screen
"""


def main():
    pygame.init()

    screens.play("startup")
    shared_data["run"][1] = True



    load_menu("main_menu")
    while shared_data["run"][0]:
        event = shared_data["events"]

        pos = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()

        if key[pygame.K_F5]:
            shared_data["run"][1] = True
            shared_data["draw_q"].clear()

            menu = shared_data["menu"]
            shared_data["menu"] = ''
            
            load_menu(menu)
            shared_data["screen"] = [shared_data["window"].get_size()[0],
                                      shared_data["window"].get_size()[0],
                                      shared_data["window"].get_flags()]
        elif key[pygame.K_ESCAPE] and shared_data["menu"] != 'main_menu':
            load_menu('main_menu')


        for element in shared_data["actives"]:
            if isinstance(element, (Button, Label)):
                element.update(pos, event)




render_t = threading.Thread(target=render.main, name="RenderThread")
main_t = threading.Thread(target=main, name="MainThread")

main_t.start()
render_t.start()

render_t.join()
main_t.join()