# NTVFS — See related docs at docs/nucle.os/files/ntvfs.md

import struct



class FileSystem:
    MAGIC = b'NUFS'
    def __init__(self):
        self.root = FileSystem.FSNode('/', is_file=False)


    class FSNode:
        def __init__(self, name, is_file=False):
            self.name:      str         = name
            self.is_file:   bool        = is_file
            self.children:  dict        = {}
            self.path:      str         = ""
            self.link:      str|None    = None

            self.location:  bytes|None  = None


    def create_from_path(self, path: str):
        if not isinstance(self.root, FileSystem.FSNode):
            self.root = FileSystem.FSNode('/', is_file=False)

        spath = path.split('/')

        node = self.root

        for part in spath:
            if part not in node.children:
                node.children[part] = FileSystem.FSNode(part)

            

    def _reconstruct_fs(self, path_to_ntvfs):
        def read_dt_sector(data):
            size = struct.unpack('<I', data.read(4))[0]

            offset = struct.unpack('<H', data.read(2))[0]
            file_id = struct.unpack('<I', data.read(offset))[0]

            offset = struct.unpack('<H', data.read(2))[0]
            file_path = struct.unpack(f'{offset}s', data.read(offset))

            offset = struct.unpack('<H', data.read(2))[0]
            file_location = struct.unpack('<L', data.read(offset))[0]

            offset = struct.unpack('<I', data.read(4))[0]
            metadata = struct.unpack(f'{offset}s', data.read(offset))

            return {
                "sector_size":      size,
                "file_id":          file_id,
                "file_location":    file_location,
                "file_path":        file_path,
                "metadata":         metadata
            }


        try:
            data_table = []
            with open(path_to_ntvfs, 'rb') as f:
                magic = struct.unpack('4s', f.read(4))[0]

                if magic != self.MAGIC:
                    print('INVALID FILE')
                    return -1

                data_table_size = struct.unpack('<I', f.read(8))[0]


                while f.tell() < data_table_size + 8:
                    data_table.append(read_dt_sector(f))

            node = FileSystem.FSNode('/', is_file=False)

            for sector in data_table:
                spath = sector['file_path'].split('/')

                for part in spath:
                    if part not in node.children:
                        node.children[part] = FileSystem.FSNode('/', is_file=False)



        except Exception as e:
            print(e)
