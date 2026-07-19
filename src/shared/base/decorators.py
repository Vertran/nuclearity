class Dec:
    def __init__(self, log) -> None:
         self.log = log

    def _base_event_decorator(self, start_tpl, end_tpl=None, is_format=True):
            def decorator(func):
                def wrapper(obj, *args, **kwargs):
                    if is_format:
                        name = obj.__class__.__name__
                        self.log.info(start_tpl.format(name), stack_offset=3)
                    else:
                        self.log.info(start_tpl, stack_offset=3)
                    
                    
                    res = func(obj, *args, **kwargs)
                    
                    if end_tpl:
                        if is_format:
                            self.log.info(end_tpl.format(name), stack_offset=3) #type: ignore
                        else:
                            self.log.info(end_tpl, stack_offset=3)
                    return res
                return wrapper
            return decorator

    def init(self):
        return self._base_event_decorator("Initialising {}...", "{} initialised successfully")

    def kill(self):
        return self._base_event_decorator("Killing {}...", "{} terminated")

    def reinit(self):
        return self._base_event_decorator("Reinitialising {}...", "{} reinitialised successfully")

    def sub(self, event):
        return self._base_event_decorator(f"Subscribed event {event}", is_format=False)

    def unsub(self, event):
        return self._base_event_decorator(f"Unsubscribed event {event}", is_format=False)