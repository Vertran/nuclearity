from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.logger import Logger

log: "Logger | None" = None

managers: dict = {
    "video": None,
    "audio": None,
    "internet": None,
    "console": None,
    "object": None,
}

state: dict = {
    "running": True,
    "drawing": True,
}


class OBJECT(Enum):
    # ==> primitives
    CIRCLE = "circle"
    RECT = "rect"
    LINE = "line"
    TRIANGLE = "triangle"

    # ==> objects
    BUTTON = "btn"
    INPUT_FIELD = "input_field"
    LABEL = "label"
    TEXT_FIELD = "text"


screen = {}
