from enum import Enum
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from modules.logger import Logger
    from modules.managers.event_manager import EventManager
    from modules.managers.game_manager import GameManager

log: "Logger | None" = None

event_bus: "EventManager | None" = None

game_manager: "GameManager | None" = None

state: dict = {
    "running": True,
    "drawing": True,
}

class OBJECT(Enum):
#==> primitives
    CIRCLE = 'circle'
    RECT = 'rect'
    LINE = 'line'
    TRIANGLE = 'triangle'

#==> objects
    BUTTON = 'btn'
    INPUT_FIELD = 'input_field'
    LABEL = 'label'
    TEXT_FIELD = 'text'

screen = {}

os = None


def life(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            life_manager = managers.get('life')

            life_manager.fix_error(e) #type: ignore

            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                log.error('Error not fixed: ', e) #type: ignore

manager: Callable[..., Any] = None #type: ignore

class INIT:
    FULL = [
        'logger',
        #'file',
        'life',
        'console',
        'object',
        'video',
        'audio',
        'network',
        'virtOS',
        ]
    LOG = ['logger']
    #FILES = [
        #'logger',
        #'file',
        #]
    CONSOLE = [
        'logger',
        #'file',
        'console',
        ]