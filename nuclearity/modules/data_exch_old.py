import json
from logger import make_log
from letters import TEXT
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glfw
import os

__all__ = ["COLORS", "shared_data", "UI_Element"]


root_path = os.path.dirname(os.path.dirname(__file__))

with open(f"{root_path}\\sys\\settings.json") as file:
    settings = json.load(file)

shared_data = {
    "run": [True, [True, False]], #Full, [Overlay, 3D]
    "menu": "main_menu",
    "screen": [*settings["screen"]["resolution"]],
    "window": None,
    "cursor_fixation": settings["gameplay"]["cursor_fixation"],
    "UI_elements": [],
    "root_path": root_path
}

print(shared_data['screen'], shared_data['cursor_fixation'])


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
            pass

    def is_clicked(self):
        pass


class Filler():
    def __init__(self, rect, color):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        if len(color) == 3:
            color.append(255)
        self.color = color

    def draw(self):
        center = [self.width/2, self.height[3]/2]
        pos = [self.x, self.y]

        color = [c / 255.0 for c in color]

        if len(color) == 3:
            color.append(1.0)
        
        glColor4f(*color)

        glBegin(GL_QUADS)
        glVertex2f(pos[0] - center[0], pos[1] - center[1])
        glVertex2f(pos[0] + center[0], pos[1] - center[1])
        glVertex2f(pos[0] + center[0], pos[1] + center[1])
        glVertex2f(pos[0] - center[0], pos[1] + center[1])
        glEnd()
    

class ScrollField():
    def __init__(self, rect, color, highlight):
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.color = list(color)
        self.highlight_color = highlight
        self.sub_menu = 'game'



class Button:
    def __init__(self, text, rect, size, font, color, hover, bg_color, outline, onclick='none'):
        self.action = onclick
        self.text = text
        self.x = rect[0]
        self.y = rect[1]
        self.width = int(rect[2])# if len(rect) > 2 else 0
        self.height = int(rect[3])# if len(rect) > 3 else 0
        self.size = size
        self.font = None #pygame.font.Font(font, size)
        self.color = color
        self.default_color = tuple(bg_color)
        self.outline_color = tuple(outline)
        self.bg_color = list(bg_color)
        self.hover_color = hover
        #self.surface = self.font.render(self.text, True, self.color)
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
                    case _: pass

                
        else:
            self.highlighted = False
            i = 0
            for each in self.bg_color:
                each += (self.default_color[i] - each) / 10
                each = min(255, max(0, each))
                self.bg_color[i] = each
                i += 1
    
    def draw(self):
        center = [self.width/2, self.height/2]
        pos = [self.x, self.y]

        color = [c / 255.0 for c in self.bg_color]

        if len(color) == 3:
            color.append(1.0)
        
        glColor4f(*color)
        glBegin(GL_QUADS)
        glVertex2f(pos[0] - center[0], pos[1] - center[1])
        glVertex2f(pos[0] + center[0], pos[1] - center[1])
        glVertex2f(pos[0] + center[0], pos[1] + center[1])
        glVertex2f(pos[0] - center[0], pos[1] + center[1])
        glEnd()
    
class Label:
    def __init__(self, text, position, font, size, color):
        self.text = TEXT(position, color, size, text)
        self.x = position[0]
        self.y = position[1]
        self.size = size
        if font == "":
            self.font = None #pygame.font.SysFont(None, size)
        else:
            self.font = None #pygame.font.Font(None, size)
        self.color = color
        #self.surface = self.font.render(self.text, True, self.color)
        self.offset = [0, 0]

    def draw(self):
        color = [c / 255.0 for c in self.color]

        if len(color) == 3:
            color.append(1.0)
        
        glColor4f(*color)

        self.text.draw()

        


class UI_Element:
    def __init__(self, element_type, **kwargs):
        self.type = element_type
        self.rect = kwargs.get('rect', [0, 0, 0, 0])
        self.outline = kwargs.get('outline', [0, 0, 0])
        self.color = kwargs.get('color', [255, 255, 255])
        self.hover_color = kwargs.get('hover_color', [200, 200, 200])
        self.text = kwargs.get('text', '')
        self.text_color = kwargs.get('text_color', [0, 0, 0])
        self.font = kwargs.get('font', ['Arial', 12])
        self.action = kwargs.get('action', None)
        self.menu = shared_data["menu"]
        self.sub_menu = shared_data["sub_menu"]

    def load_menu(self):
        with open(".\\sys\\layouts copy.json", "r") as file:
            try:
                data = json.load(file)
                if not data:
                    raise ValueError("The JSON file is empty.")
                print(data)
                preset = data[self.menu]
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON file: {e}")
            except KeyError:
                raise ValueError(f"Menu '{self.menu}' not found in the JSON file.")

        ui = shared_data["UI_elements"]
        for element in preset:
            match element["type"]:
                case "filler":
                    ui.append(Filler(element['rect'], element['color']))
                case "button":
                    ui.append(Button(element['text'], element['rect'], element['font'][1], element['font'][0], element['color'], element['hover_color'], element['outline'], element['action']))
                    ui.append(Label(element['text'], [element['rext'][0], element['rect'][1]], element['font'][0], element['font'][1], element['text_color']))
                case "label":
                    ui.append(Label(element['text'], [element['pos'][0], element['pos'][1]], element['font'][0], element['font'][1], element['text_color']))
                case "scroll_field":
                    ui.append(ScrollField(element['rect'], element['color'], [0, 0, 0]))
                    self.load_sub()
                case _:
                    raise ValueError(f"Unknown UI element type: {element['type']}")
    
    def load_sub(self):
        with open(".\\sys\\layouts.json", "r") as file:
            preset = json.load(file)[self.menu]["menus"][self.sub_menu]
        
        ui = shared_data["UI_elements"]
        for element in preset:
            match element["type"]:
                case "button":
                    ui.append(Button(element['text'], element['rect'], element['font'][1], element['font'][0], element['color'], element['hover_color'], element['outline'], element['action']))
                case "label":
                    ui.append(Label(element['text'], [element['pos'][0], element['pos'][1]], element['font'][0], element['font'][1], element['text_color']))
                case "input":
                    ui.append(Input(element['rect'], element['color'], element['type']))
                case _:
                    raise ValueError(f"Unknown UI element type: {element['type']}")

class FileSys:
    def __init__(self, state, search_level=3):
        self.root = shared_data['root_path']
        self.state = state
        self.level = search_level
        self.settings_p = ''
        self.def_settings_p = ''

    def save(self):
        with open(self.settings_p, 'w') as file:
            file = shared_data['settings']

    def reset(self):
        with open(self.settings_p, 'w') as file:
            file = self.def_settings_p


#load_menu(shared_data["menu"])
make_log("INFO", "DataSharing started successfully")