#=== Imports Block ===#
import json
from logger import make_log
from letters import TEXT
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glfw

__all__ = ["COLORS", "shared_data", "UI_Element", "Menu", "normalize_color"]

#=== Shared Data Block ===#
# Use this data between different modeles
shared_data = {
    "run": [True, [True, False]], #Full, [Overlay, 3D]
    "menu": "main", # Current menu. Can be None
    "sub_menu": "", # Current sub-menu. Depends on menu
    "screen": [1920, 1000], # Screen res
    "cursor_fixation": False, # Is camera fixed to cursor
    "UI_elements": [] # Elements that will be drawn on screen
}

def normalize_color(color):
    return [c / 255.0 for c in color]

#=== Classes BLock ===#
# Colors. Used in [import *]. Will be normalized to 0-1 range
class COLORS:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

# UI Sub-Blocks. Buttons, Labels, Inputs, Filler, etc.
class UI_Element():
    def __init__(self, **kwargs):
        self.type = kwargs.get("type", "button")
        match self.type:
            case "button":
                self.actioon = kwargs.get("action", None)
                self.text = kwargs.get("text", "Button")
                self.font_size = kwargs.get("font_size", 18)
                rect = kwargs.get("rect", [0, 0, 0, 0])
                self.x = rect[0]
                self.y = rect[1]
                self.width = rect[2]
                self.height = rect[3]
                self.bg_color = kwargs.get("bg_color", COLORS.WHITE)
                self.color = self.bg_color
                self.hover_color = kwargs.get("hover_color", COLORS.GREEN)
                self.text_color = kwargs.get("text_color", COLORS.BLACK)
                self.pressed = False
                self.bold = kwargs.get("bold", False)
            case "label":
                self.text = kwargs.get("text", "Button")
                self.font = kwargs.get("font", "Arial")
                self.font_size = kwargs.get("font_size", 18)
                self.size = kwargs.get("size", 100)
                self.text_color = kwargs.get("text_color", [0, 0, 0])
                pos = kwargs.get("pos", [0, 0, 0, 0])
                self.x = pos[0]
                self.y = pos[1]
                self.bold = kwargs.get("bold", False)
            case "filler":
                rect = kwargs.get("rect", [0, 0, 0, 0])
                self.x = rect[0]
                self.y = rect[1]
                self.width = rect[2]
                self.height = rect[3]
                self.bg_color = kwargs.get("bg_color", [0, 0, 0, 20])
                self.color = self.bg_color
            case "sub-menu":
                rect = kwargs.get("rect", [0, 0, 0, 0])
                self.x = rect[0]
                self.y = rect[1]
                self.width = rect[2]
                self.height = rect[3]
                self.bg_color = kwargs.get("bg_color", [0, 0, 0, 20])
                self.color = self.bg_color
                self.text_color = kwargs.get("text_color", [250, 250, 250, 255])

                




    # Update the elements. Style and action.
    def update(self, pos, events=None):
        mouse_x, mouse_y = pos

        # If cursor is over.
        if (self.x - self.width / 2 <= mouse_x <= self.x + self.width / 2
            and self.y - self.height / 2 <= mouse_y <= self.y + self.height / 2):
            # Fade color to [hover_color] 
            i = 0
            for each in self.color:
                each += (self.hover_color[i] - each) / 10
                each = min(255, max(0, each))
                self.color[i] = each
                i += 1
            if events is not None:
                for event in events:
                    # If mouse is pressed
                    if (event.type == glfw.MOUSEBUTTONDOWN
                        and event.button == glfw.MOUSE_BUTTON_LEFT
                        and not self.pressed):
                        self.pressed = True
                        match self.action.split("."):
                            # Start the game
                            case ["play"]:
                                shared_data["run"][1] = [False, True]
                            # Change the menu (settings, mian, etc).
                            case ["menu", *sub]:
                                # Sub-menu names
                                match sub:
                                    case ["main_menu"]:
                                        shared_data["menu"] = "main_menu"
                                    case ["settings"]:
                                        shared_data["menu"] = "settings"
                                    case ["pause"]:
                                        shared_data["menu"] = "pause"

                            case _:
                                pass
                    
                    # On mouse release
                    elif (event.type == glfw.MOUSEBUTTONUP
                          and event.button == glfw.MOUSE_BUTTON_LEFT):
                        self.pressed = False
        else:
            # Fade color to [bg_color]
            i = 0
            for each in self.color:
                each += (self.bg_color[i] - each) / 10
                each = min(255, max(0, each))
                self.color[i] = each
                i += 1

    def draw(self):
        if self.type in ["button", "filler", "checkbox"]:
            self.color = normalize_color(self.color)
            if len(self.color) == 3:
                self.color.append(1.0)

        match self.type:
            case "button":
                # Draw button
                glBegin(GL_QUADS)
                glColor4f(*normalize_color(self.color))
                glVertex2f(self.x - self.width / 2, self.y - self.height / 2)
                glVertex2f(self.x + self.width / 2, self.y - self.height / 2)
                glVertex2f(self.x + self.width / 2, self.y + self.height / 2)
                glVertex2f(self.x - self.width / 2, self.y + self.height / 2)
                glEnd()
                
                TEXT((self.x, self.y), self.text_color, self.font_size, self.text, bold=self.bold).draw()

            case "label":
                TEXT((self.x, self.y), self.text_color, self.font_size, self.text, bold=self.bold).draw()

            case "filler":
                glBegin(GL_QUADS)
                glColor4f(*normalize_color(self.color))
                glVertex2f(self.x - self.width / 2, self.y - self.height / 2)
                glVertex2f(self.x + self.width / 2, self.y - self.height / 2)
                glVertex2f(self.x + self.width / 2, self.y + self.height / 2)
                glVertex2f(self.x - self.width / 2, self.y + self.height / 2)
                glEnd()
                


class UI_SubElement():
    def __init__(self, **kwargs):
        self.type = kwargs.get("type", "label")
        match self.type:
            case "checkbox":
                rect = kwargs.get("rect", [0, 0, 0, 0])
                self.x = rect[0]
                self.y = rect[1]
                self.width = rect[2]
                self.height = rect[3]
                self.box_color = kwargs.get("box_color", [250, 250, 250])
                self.color = self.box_color
                self.destination = kwargs.get("destination", None)
                self.label = kwargs.get("label", "Anti-aliasing")

    def draw(self):
        match self.type:
            case "checkbox":
                # Draw checkbox
                glBegin(GL_QUADS)
                glColor4f(*normalize_color(self.box_color))
                glVertex2f(self.x - self.width / 2, self.y - self.height / 2)
                glVertex2f(self.x + self.width / 2, self.y - self.height / 2)
                glVertex2f(self.x + self.width / 2, self.y + self.height / 2)
                glVertex2f(self.x - self.width / 2, self.y + self.height / 2)
                glEnd()

                glBegin(GL_LINES)
                glColor4f(*normalize_color(self.box_color))
                glVertex2f(self.x + self.width / 2 - 20,
                           self.y + self.height / 2 - 20)
                glVertex2f(self.x + self.width / 2 + 20,
                           self.y + self.height / 2 - 20)
                glVertex2f(self.x + self.width / 2 + 20,
                           self.y + self.height / 2 + 20)
                glVertex2f(self.x + self.width / 2 - 20,
                           self.y + self.height / 2 + 20)
                
    def update(self):
        pass


# Menu class. Operations with menu (load).
class Menu(UI_Element):
    # Load layouts from JSON file.
    def load_menu(menu):
        if menu != shared_data["menu"]:
            with open(f".\\sys\\layouts copy.json", "r") as file:
                preset = json.load(file)[menu]

            if not preset:
                make_log("ERROR", "Menu not loaded")
                return False
            
            shared_data["menu"] = menu

            # Clear the menu
            ui = shared_data["UI_elements"] = []

            # Load menu objects to [shared_data]
            for element in preset:
                ui.append(UI_Element(**element))

            make_log("INFO", "Menu loaded:", menu)

    def load_sub(menu, sub_menu):
        if menu != shared_data["menu"]:
            with open(f".\\sys\\layouts copy.json", "r") as file:
                preset = json.load(file)[menu]["menus"]

            if not preset:
                make_log("ERROR", "Menu not loaded")
                return False
            
            shared_data["menu"] = menu

            # Clear the menu
            ui = shared_data["UI_elements"]
            ui.clear()

            for element in preset[sub_menu]["content"]:
                ui.append(UI_Element(**element))

            make_log("INFO", "Sub-menu loaded:", sub_menu)