import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log


class FSNode:
    def __init__(self, name, is_file=False):
        self.name = name
        self.is_file = is_file
        self.children = {}
        self.data = None
        self.len = self._lencalc()
    
    def get(self, path):
        parts = path.split('/')
        node = self
        for part in parts:
            node = node.children[part]
        return node

    def _lencalc(self):
        if self.data is not None:
            return len(self.name) + len(self.data)
        return len(self.name)

    def write(self, file_path):
        _file = self.get(file_path)

        if _file.is_file:
            try:
                pass
            except Exception as e:
                pass
            finally:
                self.len = self._lencalc()
        else:
            pass

    def read(self, file_path):
        _file = self.get(file_path)

        if _file.is_file:
            try:
                pass
            except Exception as e:
                pass
        else:
            pass

    def create(self, path, is_file=True):
        if self.get(path):
            log.warn('Attempted to create an existing file!')
