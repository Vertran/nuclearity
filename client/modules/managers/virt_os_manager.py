import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log

class NucleOS():
    @instancer.manager
    def __init__(self, **kwargs):
        self.configiration = self._get_config('data/settings/os.toml')
        self.filesystem = Filesystem.load('data/disk.ntvs')

        instancer.managers['virt_os'] = self


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