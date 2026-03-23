import ctypes
import math
import time

import modules.instancer as instancer
import numpy as np
from OpenGL.GL import *  # type: ignore
from PIL import Image

assert instancer.log is not None
log = instancer.log


class ObjectDrawable2D:
    def __init__(self):
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.vertices = []

        self.base_color = [1.0, 1.0, 1.0]
        self.outline_color = [1.0, 1.0, 1.0]
        self.hover_base_color = [1.0, 1.0, 1.0]
        self.hover_outline_color = [1.0, 1.0, 1.0]
        self.hover_factor = 0.0
        self.image_texture = False

    def get_uniforms(self):
        return {
            "base": self.base_color,
            "out": self.outline_color,
            "hBase": self.hover_base_color,
            "hOut": self.hover_outline_color,
            "state": self.hover_factor,
            "use_texture": 1 if self.image_texture else 0,
        }

    def load_texture(self, path):
        try:
            img = Image.open(path).convert("RGBA")
            data = img.tobytes()

            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        except Exception as e:
            log.error("An Error occured while loading the texture:", str(e))

    def upload(self):
        if not isinstance(self.vertices, np.ndarray):
            self.vertices = np.array(self.vertices, dtype=np.float32)

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        stride = 6 * 4
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        glBindVertexArray(0)

        log.info(f"Successfully uploaded verticies of {self.name} to GPU")  # type: ignore

    def draw(self):
        pass


class RegularPolygon(ObjectDrawable2D):
    def __init__(self, **kwargs):
        super().__init__()

        pos = kwargs.get("pos", [0, 0])
        self.x = pos[0]
        self.y = pos[1]
        self.radius = kwargs.get("radius", 50)

        self.name = kwargs.get("name", "NameNotProvided")

        self.color = kwargs.get("name", [0, 0, 0])

        if max(self.color) > 1.0:
            self.color = [col / 255 for col in self.color]
        else:
            self.color = list(self.color)

        self.segments = min(max(3, kwargs.get("segments", 8)), 48)

        verts = []

        for i in range(self.segments):
            theta1 = 2.0 * math.pi * i / self.segments
            theta2 = 2.0 * math.pi * (i + 1) / self.segments

            verts.extend([self.x, self.y, 0.0, 0.0, 0.0])
            verts.extend(
                [self.x + self.radius * math.cos(theta1), self.y + self.radius * math.sin(theta1), 0.0, 1.0, 0.0]
            )
            verts.extend(
                [self.x + self.radius * math.cos(theta2), self.y + self.radius * math.sin(theta2), 0.0, 1.0, 1.0]
            )

        self.vertices = np.array(verts, dtype=np.float32)

        self.upload()

    def draw(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, self.segments * 3)


class Rect(ObjectDrawable2D):
    def __init__(self, **kwargs):
        super().__init__()

        self.centered = kwargs.get("centered", [False, False])
        pos = kwargs.get("pos", [0, 0])

        self.x = pos[0] + self.centered[0] * instancer.screen["fdim"][0] / 2
        self.y = pos[1] + self.centered[1] * instancer.screen["fdim"][1] / 2

        dim = kwargs.get("dim", [0, 0])
        self.width = dim[0]
        self.height = dim[1]

        color = kwargs.get("base_color", [0, 0, 0])

        self.name = kwargs.get("name", "nameNotProvided")

        if max(color) > 1.0:
            self.base_color = [col / 255 for col in color]
        else:
            self.base_color = list(color)

        self.current_color = self.base_color.copy()

        self.image_texture = kwargs.get("image_texture", False)
        self.image_opacity = kwargs.get("image_opacity", 0)

        hw = self.width / 2
        hh = self.height / 2

        hw = self.width / 2
        hh = self.height / 2

        #           X               Y               Z       U    V      Border
        self.vertices = [
            self.x - hw,
            self.y - hh,
            0.0,
            0.0,
            0.0,
            1.0,
            self.x + hw,
            self.y - hh,
            0.0,
            1.0,
            0.0,
            1.0,
            self.x + hw,
            self.y + hh,
            0.0,
            1.0,
            1.0,
            1.0,
            self.x - hw,
            self.y - hh,
            0.0,
            0.0,
            0.0,
            1.0,
            self.x + hw,
            self.y + hh,
            0.0,
            1.0,
            1.0,
            1.0,
            self.x - hw,
            self.y + hh,
            0.0,
            0.0,
            1.0,
            1.0,
        ]

        self.vertex_count = len(self.vertices) // 6

        if self.image_texture != False:
            self.load_texture(self.image_texture)

        print(f"Rect '{self.name}': x={self.x}, y={self.y}, w={self.width}, h={self.height}")
        print(f"vertices count: {self.vertex_count}")
        print(f"vertices: {self.vertices}")

        self.upload()

    def draw(self):
        if self.image_texture:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)


class Line(ObjectDrawable2D):
    def __init__(self, **kwargs):
        super().__init__()

        pos = kwargs.get("pos", [[1920, 1080], [0, 0]])
        x1, y1 = pos[0]
        x2, y2 = pos[1]

        self.color = kwargs.get("color", [200, 200, 200])

        if max(self.color) > 1.0:
            self.color = [col / 255 for col in self.color]
        else:
            self.color = list(self.color)

        self.name = kwargs.get("name", "NameNotProvided")

        dx = x2 - x1
        dy = y2 - y1

        dist = math.sqrt(dx * dx + dy * dy)
        if dist == 0:
            return

        self.thickness = kwargs.get("thickness", 2)

        offset_x = -dy * (self.thickness / 2) / dist
        offset_y = dx * (self.thickness / 2) / dist

        p1 = [x1 + offset_x, y1 + offset_y, 0.0, *self.color]
        p2 = [x1 - offset_x, y1 - offset_y, 0.0, *self.color]
        p3 = [x2 - offset_x, y2 - offset_y, 0.0, *self.color]
        p4 = [x2 + offset_x, y2 + offset_y, 0.0, *self.color]

        self.vertices = np.array(p1 + p2 + p3 + p1 + p3 + p4, dtype=np.float32)

        self.upload()

    def draw(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices) // 6)


class Label:
    def __init__(self) -> None:
        pass


class Button(ObjectDrawable2D):
    def __init__(
        self, **kwargs
    ):  # pos=(0,0), dim=(200, 100), color=(1.0, 0.6, 0.1), thicickness=3, out_color=(1.0, 1.0, 1.0), centered=[False, False],
        super().__init__()

        def _normalize(color):
            if max(color) > 1.0:
                col = [c / 255 for c in color]
            else:
                col = list(color)
            return col

        self.centered = kwargs.get("centered", [False, False])
        pos = kwargs.get("pos", [0, 0])

        self.x = pos[0] + self.centered[0] * instancer.screen["fdim"][0] / 2
        self.y = pos[1] + self.centered[1] * instancer.screen["fdim"][1] / 2

        dim = kwargs.get("dim", [300, 200])
        self.width = dim[0]
        self.height = dim[1]

        self.base_color = _normalize(kwargs.get("base_color", [250, 40, 40]))

        self.outline_color = _normalize(kwargs.get("outline_color", [250, 40, 40]))

        self.current_color = self.base_color.copy()
        self.current_outline_color = self.outline_color.copy()

        self.hover_base_color = self.base_color
        self.hover_outline_color = self.outline_color

        self.image_texture = kwargs.get("image_texture", False)
        self.image_opacity = kwargs.get("image_opacity", 0)

        self.name = kwargs.get("name", "NameNotProvided")

        hover = kwargs.get("hover", {})
        for attr, value in hover.items():
            setattr(self, f"hover_{attr}", value)

        self.outline_thickness = kwargs.get("outline_thickness", 1)

        self.hover_factor = 0.0

        hw = self.width / 2
        hh = self.height / 2

        thic = self.outline_thickness

        #           X                      Y                      Z       U    V      Border
        self.vertices = [
            self.x - hw,
            self.y - hh,
            0.0,
            0.0,
            0.0,
            0.0,
            self.x + hw,
            self.y - hh,
            0.0,
            1.0,
            0.0,
            0.0,
            self.x + hw,
            self.y + hh,
            0.0,
            1.0,
            1.0,
            0.0,
            self.x - hw,
            self.y - hh,
            0.0,
            0.0,
            0.0,
            0.0,
            self.x + hw,
            self.y + hh,
            0.0,
            1.0,
            1.0,
            0.0,
            self.x - hw,
            self.y + hh,
            0.0,
            0.0,
            1.0,
            0.0,
            self.x - hw + thic,
            self.y - hh + thic,
            0.0,
            0.0,
            0.0,
            1.0,
            self.x + hw - thic,
            self.y - hh + thic,
            0.0,
            1.0,
            0.0,
            1.0,
            self.x + hw - thic,
            self.y + hh - thic,
            0.0,
            1.0,
            1.0,
            1.0,
            self.x - hw + thic,
            self.y - hh + thic,
            0.0,
            0.0,
            0.0,
            1.0,
            self.x + hw - thic,
            self.y + hh - thic,
            0.0,
            1.0,
            1.0,
            1.0,
            self.x - hw + thic,
            self.y + hh - thic,
            0.0,
            0.0,
            1.0,
            1.0,
        ]

        self.vertex_count = len(self.vertices) // 6

        if self.image_texture != False:
            self.load_texture(self.image_texture)

        self.upload()

    def draw(self):
        if self.image_texture:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def update(self, **kwargs):
        cur_x, cur_y = kwargs.get("cur_pos", [0, 0])
        is_hover = abs(self.x - cur_x) <= self.width / 2 and abs(self.y - cur_y) <= self.height / 2

        target = 1.0 if is_hover else 0.0

        diff = target - self.hover_factor
        if abs(diff) > 0.001:
            self.hover_factor += diff * 0.25


class InputField(ObjectDrawable2D):
    def __init__(self):
        super().__init__()
        pass
