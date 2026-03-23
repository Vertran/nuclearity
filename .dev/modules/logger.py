import inspect
import os
import time

import modules.instancer as instancer

log_path = f".logs/client/{time.strftime('%Y-%m-%d_%H-%M-%S')}.log"

os.makedirs(".logs/client", exist_ok=True)


class Logger:
    def __init__(self):

        self.session_logs = []
        self.log_path = log_path

        instancer.log = self

        instancer.log.info("Logger initialized")

    def info(self, text="", desc="", offset=4):
        self._make_log("info", message=text, description=desc, offset=offset)

    def debug(self, text="", desc="", offset=4):
        self._make_log("debug", message=text, description=desc, offset=offset)

    def warn(self, text="", desc="", offset=4):
        self._make_log("warn", message=text, description=desc, offset=offset)

    def error(self, text="", desc="", offset=4):
        self._make_log("error", message=text, description=desc, offset=offset)

    def on_kill(self, text="The last message", desc="", offset=4):
        self._make_log("kill", message=text, description=desc, offset=offset)

    def custom(self, text='', desc='', formula='', offset=4):
        self._make_log("kill", message=text, description=desc, formula=formula, offset=offset)

    def get_session_logs(self):
        return self.session_logs

    def _make_log(self, level="DEBUG", message="Debug", description=None, timestamp=None, formula=None, offset=4):
        stack = inspect.stack()

        caller_frame = stack[2]
        module = os.path.basename(caller_frame.filename)

        if timestamp is None:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if formula:
            try:
                log_entry = formula.format(**locals())
            except KeyError as e:
                log_entry = f"Error occured while making this log entry (that's ironic lol): {formula}"
                description = str(e)
        else:
            log_entry = f"\n[{timestamp}] [{module:^11}] [CLIENT] [{level.upper():^6}] {message}"

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
