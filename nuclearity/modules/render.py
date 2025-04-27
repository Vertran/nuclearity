import pygame, time
from data_exch import *
from logger import make_log

pygame.init()

def in_menus():
    return shared_data["menu"] in ['main_menu', 'settings']

def main():
    #while shared_data["window"] is None:
    #    time.sleep(0.01)

    #screen = shared_data["window"]

    screen = pygame.display.set_mode(shared_data["screen"][:2], shared_data["screen"][2])
    pygame.display.set_caption("NUCLEARITY")
    shared_data["window"] = screen


    
    while shared_data["run"][0]:
        if shared_data["run"][1]:

            shared_data["events"] = pygame.event.get()

            for event in shared_data["events"]:
                if event.type == pygame.QUIT:
                    shared_data["run"] = [False, False]
                    make_log("INFO", "Exited app")


            if in_menus() or shared_data["menu"] == "None":
                #screen.fill((0, 0, 0))

                for element in shared_data["draw_q"]:
                    element.draw(screen)

            else:
                pass
            pygame.display.update()

    pygame.quit()

make_log("INFO", "RenderEngine started successfully")