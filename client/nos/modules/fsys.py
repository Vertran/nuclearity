import modules.instancer as instancer
import nos.modules.instancer as osi

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
            header = struct.pack(f'H{len(name_b)}s?H',
                len(name_b),
                name_b,
                self.is_file,
                len(self.children)
            )
            
            if self.is_file:
                data = self.data or b''
                return header + struct.pack(f'I{len(data)}s', len(data), data)
            else:
                return header + b''.join(child.pack() for child in self.children.values())

        @classmethod
        def unpack(cls, data: bytes, offset: int = 0):
            name_len = struct.unpack_from('H', data, offset)[0]
            offset += 2
            
            name = data[offset:offset+name_len].decode('utf-8')
            offset += name_len
            
            is_file, children_count = struct.unpack_from('?H', data, offset)
            offset += 3
            
            node = cls(name, is_file=is_file)
            
            if is_file:
                data_len = struct.unpack_from('I', data, offset)[0]
                offset += 4
                node.data = data[offset:offset+data_len]
                offset += data_len
            else:
                for _ in range(children_count):
                    child, offset = cls.unpack(data, offset)
                    node.children[child.name] = child
            
            return node, offset

        def get(self, path):
            parts = [p for p in path.split('/') if p]  # фильтруем пустые части
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
                node = node.children[part]
            return node

        def _lencalc(self):
            if self.data is not None:
                return len(self.name) + len(self.data)
            return len(self.name)
            

    def save(self, path: str):
        root_data = self.root.pack()
        header = struct.pack('4sHI', self.MAGIC, self.VERSION, len(root_data))
        with open(path, 'wb') as f:
            f.write(header + root_data)

    def get(self, path):
        return self.root.get(path)

    def create(self, path, is_file=True):
        return self.root.create(path, is_file)

    @classmethod
    def load(cls, path: str):
        with open(path, 'rb') as f:
            raw = f.read()
        magic, version, root_len = struct.unpack_from('4sHI', raw)
        assert magic == cls.MAGIC, "Not a .ntvs file"
        fs = cls()
        fs.root, _ = cls.FSNode.unpack(raw, offset=8)
        return fs
