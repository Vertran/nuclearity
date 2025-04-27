__all__ = ["COLORS", "shared_data", "load_menu"]

import json, pygame
from logger import make_log

shared_data = {
    "run": [True, False], #Full, Render
    "draw_q": [],
    "draw_q_sub": [],
    "menu": "None",
    "sub_menu": [],
    "screen": [1920, 1080, pygame.FULLSCREEN],
    "window": None,
    "actives": [],
    "events": [],
    "camera_to_cursor": False
}

class COLORS:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


class Player():
    def __init__(self, pos, direction):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.direction = direction
        self.height = 1.75
        self.speed = 0.8
        self.jump = 1.2 

class Input():
    def __init__(self, rect, color, type):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.color = color
        self.type = type
        self.value = 0.5
        self.true = False

    def update(self, pos, events):
        mouse_x, mouse_y = pos

        if self.x - self.width / 2 <= mouse_x <= self.x + self.width / 2 and self.y - self.height / 2 <= mouse_y <= self.y + self.height / 2:
            self.highlighted = True
            i = 0
            for each in self.bg_color:
                each += (self.hover_color[i] - each) / 10
                each = min(255, max(0, each))
                self.bg_color[i] = each
                i += 1

            if self.is_clicked(events):
                match self.type:
                    case 'checkbox':
                        self.true = not self.true

    def draw(self, screen):
        if self.type == 'checkbox':
            pygame.draw.rect(screen, self.color, (self.x - self.width/2, self.y - self.height/2, self.width, self.height))
            if self.true:
                pygame.draw.rect(screen, (0, 255, 0), (self.x - self.width/2 + 5, self.y - self.height/2 + 5, self.width - 10, self.height - 10))
                pygame.draw.line(screen, (0, 0, 0), (self.x - self.width/2 + 5, self.y - self.height/2 + 5), (self.x + self.width/2 - 5, self.y + self.height/2 - 5), 3)

    def is_clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                return True
        return False


class Filler():
    def __init__(self, rect, color):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        if len(color) == 3:
            color.append(255)
        self.color = color

    def draw(self, screen):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.fill(self.color)

        screen.blit(surface, (self.x - self.width/2, self.y - self.height/2))
    

class ScrollField():
    def __init__(self, rect, color, highlight):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.color = list(color)
        self.highlight_color = highlight
        self.sub_menu = 'game'

    def update(self, events):
        pass

    def draw(self, screen):
        #screen.fill((100, 100, 100))
        if shared_data["menu"] == 'settings':
            opaqueSurf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            opaqueSurf.fill(self.color)

            screen.blit(opaqueSurf, (self.x - self.width/2, self.y - self.height/2))
    



class Button:
    def __init__(self, text, rect, size, font, color, hover, bg_color, outline, onclick='none'):
        self.action = onclick
        self.text = text
        self.x = rect[0]
        self.y = rect[1]
        self.width = int(rect[2])# if len(rect) > 2 else 0
        self.height = int(rect[3])# if len(rect) > 3 else 0
        self.font = pygame.font.Font(font, size)
        self.color = color
        self.default_color = tuple(bg_color)
        self.outline_color = tuple(outline)
        self.bg_color = list(bg_color)
        self.hover_color = hover
        self.surface = self.font.render(self.text, True, self.color)
        self.highlighted = False
        self.offset = [0, 0]

    def update(self, pos, event):
        mouse_x, mouse_y = pos

        if self.x - self.width / 2 <= mouse_x <= self.x + self.width / 2 and self.y - self.height / 2 <= mouse_y <= self.y + self.height / 2:
            self.highlighted = True
            i = 0
            for each in self.bg_color:
                each += (self.hover_color[i] - each) / 10
                each = min(255, max(0, each))
                self.bg_color[i] = each
                i += 1

            if self.is_clicked(event):
                self.bg_color = [200, 200, 200]
                match self.action:
                    case 'start_game':
                        shared_data["menu"] = "None"
                        shared_data["draw_q"].clear()
                    case 'settings':
                        load_menu('settings')
                    case 'exit':
                        self.bg_color = [250, 200, 200]
                        shared_data["run"] = [False, False]
                        make_log('INFO', 'Exited app')
                    case 'back':
                        load_menu('main_menu')
                    case 'settings.game':
                        ScrollField.sub_menu = 'game'
                        load_submenu('game')
                        make_log('INFO', 'Sub_menu switched to: game')
                    case 'settings.controls':
                        ScrollField.sub_menu = 'controls'
                        load_submenu('controls')
                        make_log('INFO', 'Sub_menu switched to: controls')
                    case 'settings.graphics':
                        ScrollField.sub_menu = 'graphics'
                        load_submenu('graphics')
                        make_log('INFO', 'Sub_menu switched to: graphics')
                    case 'settings.sound':
                        ScrollField.sub_menu = 'sound'
                        load_submenu('sound')
                        make_log('INFO', 'Sub_menu switched to: sound')

                
        else:
            self.highlighted = False
            i = 0
            for each in self.bg_color:
                each += (self.default_color[i] - each) / 10
                each = min(255, max(0, each))
                self.bg_color[i] = each
                i += 1

    def draw(self, screen):
        if self.highlighted:
            pygame.draw.rect(screen, self.bg_color, (self.x - self.width/2, self.y - self.height/2, self.width, self.height))
            pygame.draw.rect(screen, self.outline_color, (self.x - self.width/2 - 2, self.y - self.height/2 - 2, self.width + 2, self.height + 2), 2)
        else:
            pygame.draw.rect(screen, self.bg_color, (self.x - self.width/2, self.y - self.height/2, self.width, self.height))
        screen.blit(self.surface, self.surface.get_rect(center=(self.x, self.y)))

    def is_clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                return True
        return False
    
class Label:
    def __init__(self, text, position, font, size, color):
        self.text = text
        self.x = position[0]
        self.y = position[1]
        self.size = size
        if font == "":
            self.font = pygame.font.SysFont(None, size)
        else:
            self.font = pygame.font.Font(None, size)
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)
        self.offset = [0, 0]

    def update(self, tmp1, tmp2):
        pass

    def draw(self, screen):

        screen.blit(self.surface, self.surface.get_rect(center=(self.x, self.y)))


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
                case "image":
                    obj = [pygame.image.load(element["path"]),
                           [element["pos"][0],
                            element["pos"][1]]]
                    obj[0] = pygame.transform.scale(obj, (element["width"], element["height"]))
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