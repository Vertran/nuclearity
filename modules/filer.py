import modules.instancer as instancer
log = instancer.log
filer = instancer.filer

log.info("loading filer module")

class Filer:
    def __init__(self):
        log.info("initializing filer module worker")

        self.opened_file = None

        instancer.filer = self

    def get_opened_file(self):
        log.info("giving requested opened file")
        return self.opened_file

    def open_frames(self, path):
        log.info(f"opening text file: {path}")
        try:
            with open(path, 'r') as f:
                self.opened_file = f.read()
        except Exception as e:
            log.error(f"failed to open text file: {path} with error:", f"{e}")
            self.opened_file = None

        if self.opened_file is not None:
            ready = []
            ready_l = ""
            images = self.opened_file.split('&=-NEW-=&')
            for image in images:
                for line in image.splitlines():
                    ready_l += line + '\n'
                ready.append(ready_l)
                ready_l = ""
            return ready
        else:
            return None


    def open_style(self, path):
        type = path.split('.')[-1]
        log.info(f"opening style file: {path} of type: {type}")
        try:
            if type == 'yaml':
                import yaml
                with open(path, 'r') as f:
                    self.opened_file = yaml.safe_load(f)
            elif type == 'json':
                import json
                with open(path, 'r') as f:
                    self.opened_file = json.load(f)
            else:
                log.error(f"unsupported file type: {type}")
                self.opened_file = None
        except Exception as e:
            log.error(f"failed to open style file: {path} with error:", f"{e}")
            self.opened_file = None

        return self.opened_file

    def get_submenu(self, submenu):
        if self.opened_file is None:
            log.error('no file opened in Filer worker')

    def save_style(self, path, data):
        type = path.split('.')[-1]
        log.info(f"saving style file: {path} of type: {type}")
        try:
            if type == 'yaml':
                import yaml
                with open(path, 'w') as f:
                    yaml.dump(data, f)
            elif type == 'json':
                import json
                with open(path, 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                log.error(f"unsupported file type: {type}")
        except Exception as e:
            log.error(f"failed to save style file: {path} with error:", f"{e}")

    def kill(self):
        log.info('killing filer')
        self.opened_file = None
        instancer.filer = None
        log.info('killed filer. Bye')
