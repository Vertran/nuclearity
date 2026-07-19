from datetime import datetime
from pathlib import Path
from collections import deque

import os
import time
import inspect

from shared.base.singleton import Base as SingletonBase
from shared.base.classes import NucEvent, NucLog

class LogManager(SingletonBase):
    log_pool = deque()
    def __init__(self, cfg_path) -> None:
        self.opened_file = None
        self.state = "preinit" #preinit|run|stop|restart
        self.is_busy = False
        self.restart = False


        self.config = self._open_cfg(cfg_path)
        
        if self.config.get('split-files', False):
            self.iter = 0
            self.file_postfix = self.config.get('split-postfix', '__pt_')

        self.file_name_initial = datetime.now().strftime(self.config.get('filename-fmt', "%Y-%m-%d %H:%M:%S"))
        self.cache = {
            "modules": {}
        }

        self._open_log_file()

    def _open_cfg(self, path: Path|str) -> dict:
        import jstyleson as jsonc
        with open(path, 'r', encoding='utf-8') as file:
            return jsonc.load(file)

    def _make_log(
            self, typo: str,
            level: str,
            module: str|None,
            error_message: str,
            description = "",
            **kwargs
            ) -> None:
        match typo:
            case 'log':
                if module is None:
                    if not self.cache['modules'][self.__class__]:
                        stack = inspect.stack()

                        caller_frame = stack[2]
                        module = os.path.basename(caller_frame.filename)

                        module = "".join(word.capitalize() for word in module[:-3].split("_"))

                        self.cache['modules'][self.__class__] = module
                    
                    module = self.cache['modules'][self.__class__]

                entry = NucLog(level, module, error_message, datetime.now().strftime(""), description)
                
                if self.state != "stop":
                    self.add_to_pool(entry)
                else:
                    print(entry)

    def _open_log_file(self):
        if self.opened_file is not None:
            self._make_log('LOG', 'WARN', "LogManager", "Log file is already open. Trying to close it and open the other")
            self.restart = "restart"
            self._close_log_file()
        
        if self.config.get('split-files', False):
            file_name = self.file_name_initial + self.config.get('split-postfix', '__pt_') + str(self.iter + 1)
        else:
            file_name = self.file_name_initial
        self.opened_file = open(file_name, 'a', encoding='utf-8')



    def _close_log_file(self, forsed=[False,False], itera=0):
        import time
        if self.opened_file is not None:
            if forsed[0] and forsed[1] or itera == 5:
                self.opened_file.close()
            elif self.is_busy or len(self.log_pool) > 0:
                self.state = "stop"
                time.sleep(5)
                self._close_log_file(itera=itera+1)
            else:
                self.opened_file.close()

    def get_from_pool(self) -> NucEvent|NucLog|None:
        if len(self.log_pool) > 0:
            entry = self.log_pool[0]
            self.log_pool.popleft()
            return entry
        else:
            return None

    def add_to_pool(self, entry: NucEvent|NucLog) -> int:
        self.log_pool.append(entry)
        return 0

    
    def life_cycle(self):
        self.state = "run"
        while self.state != "stop":
            entry = self.get_from_pool()

            if entry is not None:
                self.is_busy = True

                if self.state == "restart":
                    time.sleep(0.2)

                self.opened_file.write(entry)

            time.sleep(0.2)