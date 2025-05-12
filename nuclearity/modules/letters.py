import glfw
from logger import make_log
from OpenGL.GL import *
from OpenGL.GLU import *

class TEXT:
    def __init__(self, pos, color, size, text, **kwargs):
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.size = size
        self.text = text.upper()
        self.converted = []
        self.bold = kwargs.get('bold', False)
        self.italic = kwargs.get('italic', False)
        self.underline = kwargs.get('underline', False)
        self.strike = kwargs.get('strike', False)
        self.outline = kwargs.get('outline', False)
        self.max_width = kwargs.get('max_width', 99)
        self.calc_width = 0

        max_w = 0
        for letter in self.text:
            if letter not in self.LETTERS:
                self.converted.append(self.LETTERS['UNKNOWN'])
                #raise ValueError(f"Letter '{letter}' not defined in TEXT class.")
            else:
                self.converted.append(self.LETTERS[letter])

    def draw(self):
        glColor3f(*self.color)
        max_w = 2.5
        if self.bold:
            glLineWidth(2.5)
        else:
            glLineWidth(1.5)
        glBegin(GL_LINES)
        x_offset = 0
        y_offset = 0
        for letter in self.converted:
            for line in letter:
                #if max_w < line[0][0] or max_w < line[1][0]:
                self.calc_width += max(line[0][0], line[1][0]) * self.size
                    
        for letter in self.converted:
            for line in letter:
                glVertex2f(self.x + (line[0][0] + x_offset) * self.size,
                           self.y - (line[0][1] - y_offset) * self.size)
                glVertex2f(self.x + (line[1][0] + x_offset) * self.size,
                           self.y - (line[1][1] - y_offset) * self.size)
                
            glColor3f(0.8, 0.1, 0.2)
            
            glVertex2f(self.x + x_offset * self.size - 2, self.y - y_offset * self.size)
            glVertex2f(self.x + x_offset * self.size + 2, self.y - y_offset * self.size)

            glColor3f(*self.color)
            if letter == self.LETTERS[" "]:
                x_offset += 1
            if x_offset > self.max_width:
                x_offset = 0
                y_offset += 5
            x_offset += max_w
        glEnd()


    LETTERS = {
        "UNKNOWN": [
            ((0, 0), (2, 3)), ((0, 3), (2, 0)),
            ((1, 0), (0, 1.5)), ((0, 1.5), (1, 3)),
            ((1, 3), (2, 1.5)), ((2, 1.5), (1, 0))
        ],
        " ": [],
        "A": [
            ((0, 0), (2, 3)), ((2, 3), (2, 0)),
            ((1, 1.5), (1.5, 1.5))
        ],
        "B": [
            ((0, 0), (0, 3)), ((0, 3), (2, 2)),
            ((2, 2), (0, 1.5)), ((0, 1.5), (2, 1)),
            ((2, 1), (0, 0))
        ],
        "C": [
            ((2, 0), (0, 1.5)), ((0, 1.5), (2, 3))
        ],
        "D": [
            ((0, 0), (0, 3)), ((0, 3), (2, 1.5)),
            ((2, 1.5), (0, 0))
        ],
        "E": [
            ((0, 0), (0, 3)), ((0, 3), (2, 3)),
            ((0, 1.5), (2, 1.5)), ((0, 0), (2, 0)),
        ],
        "F": [
            ((0, 0), (0, 3)), ((0, 3), (2, 3)),
            ((0, 1.5), (2, 1.5))
        ],
        "G": [
            ((1, 1), (2, 1)), ((2, 1), (2, 0)),
            ((2, 0), (0, 0)), ((0, 0), (0, 3)),
            ((0, 3), (2, 3))
        ],
        "H": [
            ((0, 0), (0, 3)), ((0, 1.5), (2, 1.5)),
            ((2, 3), (2, 0))
        ],
        "I": [
            ((0, 0), (2, 0)), ((0, 3), (2, 3)),
            ((1, 0), (1, 3))
        ],
        "J": [
            ((0, 0.5), (0, 0)), ((0, 0), (1, 0)),
            ((1, 0), (1, 3)), ((0, 3), (2, 3))
        ],
        "K": [
            ((0, 3), (0, 0)), ((0, 1.5), (2, 3)),
            ((0, 1.5), (2, 0))
        ],
        "L": [
            ((0, 3), (0, 0)), ((0, 0), (2, 0))
        ],
        "M": [
            ((0, 0), (0, 3)), ((0, 3), (1, 2)),
            ((1, 2), (2, 3)), ((2, 3), (2, 0))
        ],
        "N": [
            ((0, 0), (0, 3)), ((0, 3), (2, 0)),
            ((2, 0), (2, 3))
        ],
        "O": [
            ((1, 0), (0, 1.5)), ((0, 1.5), (1, 3)),
            ((1, 3), (2, 1.5)), ((2, 1.5), (1, 0))
        ],
        "P": [
            ((0, 0), (0, 3)), ((0, 3), (2, 2)),
            ((2, 2), (0, 1.5))
        ],
        "Q": [
            ((1, 0), (0, 1.5)), ((0, 1.5), (1, 3)),
            ((1, 3), (2, 1.5)), ((2, 1.5), (1, 0)),
            ((0.75, 1.5), (2, 0))
        ],
        "R": [
            ((0, 0), (0, 3)), ((0, 3), (2, 2)),
            ((2, 2), (0, 1.5)), ((0, 1.5), (2, 0))
        ],
        "S": [
            ((0, 1), (1, 0)), ((1, 0), (2, 1)),
            ((2, 1), (0, 2)), ((0, 2), (1, 3)),
            ((1, 3), (2, 2))
        ],
        "T": [
            ((1, 0), (1, 3)), ((0, 3), (2, 3))
        ],
        "U": [
            ((0, 3), (0, 1)), ((0, 1), (1, 0)),
            ((1, 0), (2, 1)), ((2, 1), (2, 3))
        ],
        "V": [
            ((0, 3), (1, 0)), ((1, 0), (2, 3))
        ],
        "W": [
            ((0, 3), (0.25, 0)), ((0.25, 0), (1, 3)),
            ((1, 3), (0.75, 0)), ((0.75, 0), (2, 3))
        ],
        "X": [
            ((0, 3), (2, 0)), ((0, 0), (2, 3))
        ],
        "Y": [
            ((0, 3), (1, 2)), ((1, 2), (2, 3)),
            ((1, 0), (1, 2))
        ],
        "Z": [
            ((0, 3), (2, 3)), ((2, 3), (0, 0)),
            ((0, 0), (2, 0))
        ],
        "<": [
            ((2, 0), (0, 1.5)), ((0, 1.5), (2, 3))
        ],
        ">": [
            ((0, 0), (2, 1.5)), ((2, 1.5), (0, 3))
        ],
        "-": [
            ((0, 1.5), (2, 1.5))
        ]
    }

make_log("INFO", "Letters module loaded")