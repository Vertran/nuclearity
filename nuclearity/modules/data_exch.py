__all__ = ["COLORS", "shared_data", "load_menu"]

import json
from logger import make_log
from objects import *

shared_data = {
    "run": [True, False], #Full, Render
    "draw_q": [],
    "draw_q_sub": [],
    "menu": "None",
    "sub_menu": [],
    "screen": [1920, 1080],
    "window": None,
    "actives": [],
    "events": [],
    "camera_to_cursor": False
}

def load_menu(menu):
    if menu != shared_data["menu"]:
        if (menu == 'settings' or menu == 'main_menu') and shared_data["camera_to_cursor"] != False:
            shared_data["camera_to_cursor"] = False
        elif shared_data["camera_to_cursor"] != True:
            shared_data["camera_to_cursor"] = True
        shared_data["menu"] = menu
        shared_data["draw_q"].clear()
        with open("C:\\Users\\justv\\OneDrive\\Рабочий стол\\nuclearity\\sys\\layouts.json", "r", encoding="utf-8") as file:
            layouts = json.load(file)[menu]

        make_log("INFO", f"Menu switched to: {menu}")

        for element in layouts:
            match element["type"]:
                case "filler":
                    obj = Filler(element["rect"], element["color"])
                case "button":
                    obj = Button(element["text"], element["rect"],
                                 36, None,
                                 element["text_color"],
                                 element["hover_color"],
                                 element["color"],
                                 element["outline"],
                                 element["action"])
                    shared_data["actives"].append(obj)
                case "label":
                    obj = Label(element["text"],
                                element["pos"],
                                element["font"],
                                element["size"],
                                element["text_color"])
                    shared_data["actives"].append(obj)
                #case "image":
                #    obj = [pygame.image.load(element["path"]),
                #           [element["pos"][0],
                #            element["pos"][1]]]
                #    obj[0] = pygame.transform.scale(obj, (element["width"], element["height"]))
                case "scroll-field":
                    obj1 = ScrollField(element["rect"],
                                      element["color"],
                                      element["highlight"])
                    
                    shared_data["draw_q"].append(obj1)
                    shared_data["actives"].append(obj1)
                    i = 1
                    for button in element["menus"]:
                        obj = Button(button,
                                     (160, 20+i*75, 200, 75),
                                     36, None, (255, 255, 255),
                                     (100, 100, 100), (20, 20, 20),
                                     (20, 20, 20), button[0])
                        if i < len(element["menus"]):
                            shared_data["draw_q"].append(obj)
                        shared_data["actives"].append(obj)
                        i += 1
                    load_submenu(obj1.sub_menu)
                    

                
            shared_data["draw_q"].append(obj)


def load_submenu(sub_menu):
    if sub_menu != shared_data["sub_menu"]:
        shared_data["sub_menu"] = sub_menu
        menu = shared_data["menu"]
        shared_data["draw_q"].clear()
        with open("C:\\Users\\justv\\OneDrive\\Рабочий стол\\nuclearity\\sys\\layouts.json", "r", encoding="utf-8") as file:
            layouts = json.load(file)["settings"][2]["menus"][sub_menu]

        make_log("INFO", f"Sub_menu switched to: {sub_menu}")

        for element in layouts["content"]:
            match element["type"]:
                case 'checkbox':
                    obj = Input(element["rect"], element["color"], element["type"])
                    shared_data["actives"].append(obj)
                case 'text':
                    pass
                case 'range':
                    pass
                case 'radio':
                    pass


                
            #shared_data["sub_draw_q"].append(obj)

#load_menu(shared_data["menu"])
make_log("INFO", "DataSharing started successfully")