from src.shared.modules.logger import Logger
from src.shared.decorators import Dec

class AppManager:
    log = Logger()
    dec = Dec(log)

    @dec.init()
    def __init__(self) -> None:
        self.subscribers = {}


    def init_manager(self, manager_cls, *args, **kwargs):
        return manager_cls(args, kwargs)

    @dec.sub
    def subscribe(self, event, handler):

        self.subscribers[event].update(handler)

    def emit(self, event):
        for func in self.subscribers.get(event, []):
            func()
