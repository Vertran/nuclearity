import inspect
import os
import time
from datetime import datetime

from src.shared.base.classes import *

log_path = f".logs/client/{time.strftime('%Y-%m-%d_%H-%M-%S')}.log"

os.makedirs(".logs/client", exist_ok=True)


class Logger:
    def __init__(self):
        self.curr_session = []
        self.log_path = log_path
        self.run = True
        self.is_busy = False
        self.info("Logger initialized")

    def info(self,
            text="",
            desc="",
            stack_offset=2,
            file_name=None):
        self._make_log("info", message=text, description=desc, stack_offset=stack_offset, file_name=file_name)

    def debug(self,
            text="",
            desc="",
            stack_offset=2,
            file_name=None):
        self._make_log("debug", message=text, description=desc, stack_offset=stack_offset, file_name=file_name)

    def warn(self,
            text="",
            desc="",
            stack_offset=2,
            file_name=None):
        self._make_log("warn", message=text, description=desc, stack_offset=stack_offset, file_name=file_name)

    def error(self,
            text="",
            desc="",
            stack_offset=2,
            file_name=None):
        self._make_log("error", message=text, description=desc, stack_offset=stack_offset, file_name=file_name)

    def on_kill(self,
            text="The last message",
            desc="",):
        self._make_log("kill", message=text, description=desc, stack_offset=2)

    def _make_log(self,
            level="DEBUG",
            message="Debug",
            description="",
            stack_offset=3,
            file_name=None):

        if not self.run:
            print('WARN: Logger is OFF')
            print(level, message, description)
            return

        if file_name is None:
            stack = inspect.stack()

            caller_frame = stack[stack_offset]
            module = os.path.basename(caller_frame.filename)

            module = "".join(word.capitalize() for word in module[:-3].split("_"))
        else:
            module = file_name

        new_log = NucLog(level, module, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], description)

        self.curr_session.append(new_log)
        print(new_log)

    def event(self, event, level, stack_offset=3, file_name=None):
        if file_name is None:
            stack = inspect.stack()

            caller_frame = stack[stack_offset]
            module = os.path.basename(caller_frame.filename)

            module = "".join(word.capitalize() for word in module[:-3].split("_"))
        else:
            module = file_name

        new_event = NucEvent(event, level, module, datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])

        self.curr_session.append(new_event)


    def cycle(self):
        pos = 0

        with open(self.log_path if self.log_path else log_path, 'a', encoding='utf-8') as f:
            while self.run:
                if pos <= len(self.curr_session):
                    self.is_busy = True
                    entries = self.curr_session[pos:]
                    for entry in entries:
                        f.write(entry.__repr__())
                        pos += 1
                    f.flush()
                    self.is_busy = False
                time.sleep(0.2)




    def clear_logs(self):
        if os.path.exists(log_path):
            os.remove(log_path)
            self.curr_session.clear()
            self.info("Logs cleared")
        else:
            self.warn("No log file to clear")

    def kill(self):
        self.info("killing logger")

        self.run = False

        while self.is_busy:
            time.sleep(0.1)

        self.on_kill("Logger killed. Bye")

        self.curr_session.clear()
        self.log_path = None