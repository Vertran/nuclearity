# NTVFS — See related docs at docs/nucle.os/files/ntvfs.md

from concurrent.interpreters import create
import struct

class FilesystemAPI:
    def __init__(self, fs: FileSystem):
        self._fs = fs

    def find(self, target: str):
        pass

    def make_file(self, path: str):
        self._fs._create_from_path(path)

class FileSystem:
    MAGIC = b'NUFS'
    def __init__(self):
        self._root = FileSystem.FSNode('/', is_file=False)
        self._options = {}
        self.api_call = FilesystemAPI(self)

    class FSNode:
        def __init__(self, name, is_deleted=False, is_hidden=False, is_file=False):
            self.name:      str         = name
            self.is_file:   bool        = is_file
            self.is_deleted:bool        = is_deleted
            self.is_hidden: bool        = is_hidden
            self.children:  dict        = {}
            self.path:      str         = ""
            self.link:      str|None    = None

            self.location:  bytes|None  = None



    def _create_from_path(self, path: str):
        spath = path.split('/')

        node = self._root

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

            for sector in data_table:
                self._create_from_path(sector["file_path"])



        except Exception as e:
            print(e)

    def copy_filesystem_drive(self, origin_path: str, target_path: str, IS_OVERWRITE_ALLOWED: bool = False):
        if IS_OVERWRITE_ALLOWED and self._options["FS_ACTIONS"]["OVERWRITE_REQUESTED__AND_YOURE_REALLY_SHURE_ABT_THIS"]:
            try:
                import shutil

                shutil.copy2(origin_path, target_path)

            except Exception as e:
                print("Thank The God, cuz I'm not overwriting your FS bro.\n", str(e))
