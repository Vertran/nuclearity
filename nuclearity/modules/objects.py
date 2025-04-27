__all__ = ['COLORS', 'Player', 'Input', 'Filler', 'ScrollField', 'Button', 'Label']

import glfw
from OpenGL.GL import *
from data_exch import shared_data, load_menu, load_submenu
from logger import make_log

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

    def draw(self, screen):
        pass
    

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
        if shared_data["menu"] == 'settings':
            pass



class Button:
    def __init__(self, text, rect, size, font, color, hover, bg_color, outline, onclick='none'):
        self.action = onclick
        self.text = text
        self.x = rect[0]
        self.y = rect[1]
        self.width = int(rect[2])# if len(rect) > 2 else 0
        self.height = int(rect[3])# if len(rect) > 3 else 0
        self.font = None #pygame.font.Font(font, size)
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
        pass

    def is_clicked(self, events):
        pass
    
class Label:
    def __init__(self, text, position, font, size, color):
        self.text = text
        self.x = position[0]
        self.y = position[1]
        self.size = size
        if font == "":
            self.font = None #pygame.font.SysFont(None, size)
        else:
            self.font = None #pygame.font.Font(None, size)
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)
        self.offset = [0, 0]

    def update(self, tmp1, tmp2):
        pass

    def draw(self, screen):

        screen.blit(self.surface, self.surface.get_rect(center=(self.x, self.y)))

