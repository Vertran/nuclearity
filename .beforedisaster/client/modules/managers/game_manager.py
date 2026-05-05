from modules.instancer import INIT, manager
from modules.logger import Logger
from modules.managers.audio_manager import AudioManager
from modules.managers.console_manager import Console
from modules.managers.file_manager import FileManager
from modules.managers.life_manager import LifeManager
from modules.managers.network_manager import NetworkManager
from modules.managers.object_manager import ObjectManager
from modules.managers.video_manager import VideoManager
from modules.managers.virt_os_manager import NucleOS


class GameManager:
    _registry = {
        'logger':       Logger,
        'life':         LifeManager,
        'file':         FileManager,
        'console':      Console,
        'object':       ObjectManager,
        'video':        VideoManager,
        'audio':        AudioManager,
        'network':      NetworkManager,
        'virtOS':       NucleOS,
    }


    @manager
    def __init__(self):
        self.modules = {}

        import modules.instancer as instancer

        instancer.game_manager = self

    def init(self, level=INIT.FULL, exclude=None):
        needed = self._resolve_deps(level)
        for key in needed:
            if key in (exclude or []):
                continue
            cls = self._registry[key]
            reqs_needed = getattr(cls, 'req', None)
            if reqs_needed:
                reqs = {}
                for req in reqs_needed:
                    reqs[req] = input(f'{req}?> ')
                cls(reqs)
            else:
                cls()


    def _resolve_deps(self, targets):
        needed = []
        
        def collect(key):
            cls = self._registry[key]
            for dep in getattr(cls, 'deps', []):
                collect(dep)
            if key not in needed:
                needed.append(key)
        
        for key in targets:
            collect(key)
        
        return needed

