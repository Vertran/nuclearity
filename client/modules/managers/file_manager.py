import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log


class FileManager:
    @instancer.manager
    def __init__(self):
        self.opened_files = []
        #{
        #    "pid":          None,
        #    "name":         "",
        #    "path":         "",
        #    "raw_cont":     None,
        #    "lock":         False,
        #}

        instancer.managers["file"] = self

    def open_file(self, path=''):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read()

            self.__add_opened(data)
            return data
        except Exception as e:
            log.error(f'Exception occured while opening the `{path}`:', str(e))


    def __add_opened(self, data):
        self.opened_files.append

    def kill(self, is_check=False):
        if not is_check:
            log.on_kill('Killing File Manager')

            self.opened_files.clear()