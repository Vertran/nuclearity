import modules.instancer as instancer
import nos.modules.instancer as osi

#from client.nos.kernel.submodules import dataclasses

assert instancer.log is not None
log = instancer.log

import struct


class Filesystem:
    MAGIC = b'NTVS'
    VERSION = 1

    def __init__(self):
        self.root = Filesystem.FSNode('/', is_file=False)

        osi.fs = self


    class FSNode:
        def __init__(self, name, is_file=False):
            self.name = name
            self.is_file = is_file
            self.children = {}
            self.data = None
            self.len = self._lencalc()

        def pack(self) -> bytes:
            name_b = self.name.encode('utf-8')
            header = struct.pack(f'<H{len(name_b)}s?H',
                len(name_b),
                name_b,
                self.is_file,
                len(self.children)
            )
            
            if self.is_file:
                data = self.data or b''
                return header + struct.pack(f'<I{len(data)}s', len(data), data)
            else:
                return header + b''.join(child.pack() for child in self.children.values())

        def set_data(self, path, data):
            mfile = self.get(path)
            if mfile.is_file:
                mfile.data = data
                log.info(f'changed file `{path.split('/')[-1]}`')

        @classmethod
        def unpack(cls, data: bytes, offset: int = 0):
            name_len = struct.unpack_from('<H', data, offset)[0]
            offset += 2
            
            name = data[offset:offset+name_len].decode('utf-8')
            offset += name_len
            
            is_file, children_count = struct.unpack_from('<?H', data, offset)
            offset += 3
            
            node = cls(name, is_file=is_file)
            
            if is_file:
                data_len = struct.unpack_from('<I', data, offset)[0]
                offset += 4
                node.data = data[offset:offset+data_len]
                offset += data_len
            else:
                for _ in range(children_count):
                    child, offset = cls.unpack(data, offset)
                    node.children[child.name] = child
            
            return node, offset

        def get(self, path):
            parts = [p for p in path.split('/') if p]
            node = self
            for part in parts:
                if part not in node.children:
                    return None
                node = node.children[part]
            return node

        def create(self, path, is_file=True):
            parts = [p for p in path.split('/') if p]
            node = self
            for i, part in enumerate(parts):
                if part not in node.children:
                    is_last = (i == len(parts) - 1)
                    node.children[part] = Filesystem.FSNode(part, is_file=is_last and is_file)
                    if is_file and is_last:
                        log.info(f'Created file `{part}`')
                node = node.children[part]
            return node

        def _lencalc(self):
            if self.data is not None:
                return len(self.name) + len(self.data)
            return len(self.name)

        def get_data(self):
            return self.data.decode('utf-8')
            

    def save(self, path: str):
        root_data = self.root.pack()
        header = struct.pack('<4sHI', self.MAGIC, self.VERSION, len(root_data))
        with open(path, 'wb') as f:
            f.write(header + root_data)

    def get(self, path):
        return self.root.get(path)

    def get_data(self, path):
        _file = self.root.get(path)
        if _file.is_file:
            return _file.data

    def create(self, path, is_file=True):
        return self.root.create(path, is_file)

    def fetch(self, path, ospath=None):
        if ospath is not None:
            with open(path, 'rb') as f:
                data = f.read()

            print(path)
            
            module_path = ospath.rstrip('/') + '/' + path.name
            self.root.create(module_path, is_file=True)
            self.root.set_data(module_path, data)
            return self.get(module_path)

    @classmethod
    def load(cls, path: str):
        with open(path, 'rb') as f:
            raw = f.read()
        magic, version, root_len = struct.unpack_from('<4sHI', raw)
        assert magic == cls.MAGIC, "Not a .ntvs file"
        fs = cls()
        fs.root, _ = cls.FSNode.unpack(raw, offset=10)
        return fs


    def _ls(self, path):
        node = self.root.get(path)
        if node is None:
            print(f'ls: {path}: No such file or directory')
            return
        for name, child in node.children.items():
            prefix = '/' if not child.is_file else ' '
            print(f'{prefix} {name}')

    def _cat(self, path):
        node = self.root.get(path)
        if node is None or not node.is_file:
            print(f'cat: {path}: No such file')
            return
        print(node.data.decode('utf-8'))