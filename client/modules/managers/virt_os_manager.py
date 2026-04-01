import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log

from pathlib import Path

from nos.kernel.submodules.interpreter import Interpreter
from nos.kernel.submodules.lexer import Lexer
from nos.kernel.submodules.parser import Parser
from nos.modules.fsys import Filesystem


class NucleOS():
    @instancer.manager
    def __init__(self, **kwargs):
        #self.configiration = self._get_config('data/settings/os.toml')
        self.ntvs_path = 'client/data/disk.ntvs'
        try:
            self.filesystem = Filesystem.load(self.ntvs_path)
        except:
            log.warn('No filesystem or it`s corrupted. Fallback to new')
            self.filesystem = Filesystem()

        base_path = Path("client/nos/kernel/def")

        if base_path.exists():
            for file_path in base_path.glob("*.nosc"):
                imported = self.filesystem.fetch(file_path, '/MOD')

                if imported:
                    log.info(f'Loaded `{file_path.name}`!')
        else:
            log.error('Could bot fetch test modules to NucleOS')

        instancer.managers['virt_os'] = self

        self.is_debugging = kwargs.get('is_debug', False)


        
    def boot(self):
        if self.filesystem is None:
            log.error('No filesystem!')
            return

        run = True
        _dir = '/'
        while run:
            uArg = input(f'${_dir}:> ').split(' ')
            #print(uArg)

            if len(uArg) == 1:
                uArg.append(_dir)
            match uArg[0]:
                case 'eval':
                    print(f'Starting {uArg[1]}')

                    app_path = _dir.rstrip('/') + '/' + uArg[1]


                    app_file = self.filesystem.get(app_path).get_data()
                    log.info(f'Running `{app_path}`!', app_file)
                    log.info(f'Requested to start {uArg[1]}', str(uArg))
                    tokens = Lexer().start(app_file)
                    parser = Parser(tokens)
                    parsed = parser.parse()

                    if self.is_debugging:
                        for node in parsed:
                            self._pretty_ast(node)

                    interpreter = Interpreter()
                    interpreter.run(parsed)

                case 'exit':
                    log.info('Requested to exit', str(uArg))
                    self.filesystem.save(self.ntvs_path)
                    run = False
                
                case 'echo':
                    print(uArg[1:])
                
                case 'mkfile':
                    log.info('Requested to make file', str(uArg))
                    if not uArg[1].startswith('/'):
                        uArg[1] = _dir + uArg[1]
                    self.filesystem.create(uArg[1], is_file=True)
                
                case 'mkdir':
                    log.info('Requested to make directory', str(uArg))
                    if not uArg[1].startswith('/'):
                        uArg[1] = _dir + uArg[1]
                    self.filesystem.create(uArg[1])

                case 'cd':
                    log.info('Requested to change directory', str(uArg))
                    if uArg[1] == '..':
                        _dir = '/'.join(_dir.rstrip('/').split('/')[:-1])
                        continue
                    elif uArg[1] == '/':
                        _dir = '/'
                        continue

                    if not uArg[1].startswith('/'):
                        uArg[1] = _dir + uArg[1]
                    
                    if self.filesystem.get(uArg[1]) is not None:
                        _dir += uArg[1] + '/'
                    else:
                        print('No such file')

                case 'ls':
                    log.info('Requested to list', str(uArg))
                    if not uArg[1].startswith('/'):
                        uArg[1] = _dir + uArg[1]
                    self.filesystem._ls(uArg[1])

                case _:
                    log.info('Unknown request', str(uArg))
                    print('Unknown command')


        self.filesystem.save(self.ntvs_path)


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
                            log.warn(f'Got unpredicted filetype `{filename_ext}`, but opened.', data[0:100]) #type: ignore



            return data #type: ignore
        return None

    def _pretty_ast(self, node, indent=0):
        if isinstance(node, list):  # ← и это
            for item in node:
                self._pretty_ast(item, indent)
            return

        prefix = "|  " * indent
        name = type(node).__name__
        
        if hasattr(node, '__dict__'):
            print(f"[DEBUG] {prefix}{name}")
            for key, val in node.__dict__.items():
                if isinstance(val, list):
                    print(f"[DEBUG] {prefix}  {key}:")
                    for item in val:
                        self._pretty_ast(item, indent + 2)
                elif hasattr(val, '__dict__'):
                    print(f"[DEBUG] {prefix}  {key}:")
                    self._pretty_ast(val, indent + 2)
                else:
                    print(f"[DEBUG] {prefix}  {key}: {val!r}")
        else:
            print(f"[DEBUG] {prefix}{node!r}")