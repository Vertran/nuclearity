from datetime import datetime

import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log


class FileManager:
    @instancer.manager
    def __init__(self):
        self.opened_files = []
        #{
        #    "pid":          None,
        #    "timestamp":    None,
        #    "name":         "",
        #    "path":         "",
        #    "raw_cont":     None,
        #    "lock":         False,
        #}

        instancer.managers["file"] = self

    def open(self, path, mode='r', encoding='utf-8'):
        if 'b' in mode:
            f = open(path, mode)
        else:
            f = open(path, mode, encoding=encoding)

        self.opened_files.append({
            "timestamp":    datetime.now(),
            "path":         path,
            "handle":       f,
            "lock":         True,
        })
        return f

    def close(self, path):
        self.opened_files[path]["handle"].close()
        del self.opened_files[path]

    def kill(self, is_check=False):
        if not is_check:
            log.on_kill('Killing File Manager')

            for file in self.opened_files:
                self.close(file['path'])

            self.opened_files.clear()