import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log

class NucleOS():
    @instancer.manager
    def __init__(self, **kwargs):
        self.configiration = self._get_config('data/settings/os.toml')
        self.filesystem = {}

#   === STRUCTURE ===

#       4.Bytes                         4.Bytes                         4.Bytes
#       magic               +           version             +           psize
#       NtVS                               1                               20

#       16.Bytes                        4.Bytes
#       filename            +             size
#       'virtual.file'                     40

#       4.Bytes
#       pathlen             +             path
#       32                         'path/to/virtual.file'

#       N.Bytes
#       data
#       'alalala'



    def open_NtVS_image(self, path):
        import struct

        offset = 0

        with open(path, 'rb') as f:
            data = f.read()
        magic, version = struct.unpack('4sH', data[:6])

        if magic == b'NtVS':
            while offset <= len(data):
                #=> name|size
                name, size = struct.unpack('16sI', data[offset:offset+20])
                offset += 20

                #=> pathlen|path
                path_len, = struct.unpack('I', data[offset:offset+4])
                offset += 4

                path = data[offset:offset+path_len].decode('utf-8')
                offset += path_len

                #=> data
                file_data = struct.unpack(f'{size}s', data[offset:offset+size])
                offset += size


        else:
            log.error(f'FIle `{path.split('/')[-1]}` is not a NtVS file originally.')

        


    def _get_config(self, path):
        if path:
            filename_ext = path.split('.')[-1]

            has_error = False

            match filename_ext:
                case 'toml':
                    import tomllib

                    with open(path, 'rb') as f:
                        data = tomllib.load(f)
                
                case 'json':
                    import json

                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                case _:
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            data = f.read()
                    except Exception as e:
                        log.error(f'Got an error while opening `{path}`:', str(e))
                        has_error = True
                    finally:
                        if has_error:
                            log.error('Got an error while opening file. It`s somewhere higher')
                        else:
                            log.warn(f'Got unpredicted filetype `{filename_ext}`, but opened.', data[-100:0]) #type: ignore



            return data #type: ignore
        return None