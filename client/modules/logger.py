import inspect
import os
import time
from datetime import datetime

import modules.instancer as instancer

log_path = f".logs/client/{time.strftime('%Y-%m-%d_%H-%M-%S')}.log"

os.makedirs(".logs/client", exist_ok=True)


class Logger:
    def __init__(self):

        self.session_logs = []
        self.log_path = log_path

        instancer.log = self

        def init_decorator(func):
            def wrapper(*args, **kwargs):
                name = args[0].__class__.__name__

                self.info(f'Initialising {name}', stack_offset=3, file_name=name)
                result = func(*args, **kwargs)
                self.info(f'{name} initialised successfully', stack_offset=3, file_name=name)
                
                return result
            return wrapper

        instancer.manager = init_decorator

        instancer.log.info("Logger initialized")

    def info(self,
            text="",
            desc="",
            offset=4,
            stack_offset=2,
            file_name=None):
        self._make_log("info", message=text, description=desc, offset=offset, stack_offset=stack_offset, file_name=file_name)

    def debug(self,
            text="",
            desc="",
            offset=4,
            stack_offset=2,
            file_name=None):
        self._make_log("debug", message=text, description=desc, offset=offset, stack_offset=stack_offset, file_name=file_name)

    def warn(self,
            text="",
            desc="",
            offset=4,
            stack_offset=2,
            file_name=None):
        self._make_log("warn", message=text, description=desc, offset=offset, stack_offset=stack_offset, file_name=file_name)

    def error(self,
            text="",
            desc="",
            offset=4,
            stack_offset=2,
            file_name=None):
        self._make_log("error", message=text, description=desc, offset=offset, stack_offset=stack_offset, file_name=file_name)

    def on_kill(self,
            text="The last message",
            desc="",
            offset=4,
            stack_offset=2,
            file_name=None):
        self._make_log("kill", message=text, description=desc, offset=offset, stack_offset=stack_offset, file_name=file_name)

    def get_session_logs(self):
        return self.session_logs

    def _make_log(self,
            level="DEBUG",
            message="Debug",
            description=None,
            timestamp=None,
            offset=4,
            stack_offset=3,
            file_name=None):

        if file_name is None:
            stack = inspect.stack()

            caller_frame = stack[stack_offset]
            module = os.path.basename(caller_frame.filename)

            module = "".join(word.capitalize() for word in module[:-3].split("_"))
        else:
            module = file_name


        if timestamp is None:
            now = datetime.now()
            ms = now.strftime("%f")[:2]
            timestamp = time.strftime(f"%Y-%m-%d %H:%M:%S.{ms}", time.localtime())
        
        log_entry = f"\n[{timestamp}] [{module:^11}] [{level.upper():^6}] {message}"

        if description:
            log_entry += "\n" + " " * offset + f"{description}\n"

        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)

        self.session_logs.append(log_entry)

    def clear_logs(self):
        if os.path.exists(log_path):
            os.remove(log_path)
            self.session_logs = []
            self.info("Logs cleared")
        else:
            self.warn("No log file to clear")

    def kill(self):
        self.info("killing logger")
        self.session_logs = []
        self.log_path = None

        instancer.log = None

        self.on_kill("Logger killed. Bye")
