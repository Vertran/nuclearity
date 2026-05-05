import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log

import ast
import inspect


class LifeManager:
    @instancer.manager
    def __init__(self, config_path="data/health/default.txt"):
        self.configs = self._load_configs(config_path)
        self.max_tries = 3
        self.retry_after = 3
        self.known_errors = {}

        instancer.managers["life"] = self

    def fix_error(self, e):
        fingerprint = f"{type(e).__name__}:{str(e.with_traceback)}"

        if fingerprint in self.known_errors:
            if self.known_errors[fingerprint] == "fixing":
                return
            elif self.known_errors[fingerprint] == "fixed":
                log.warn("Recurring error:", fingerprint)

        print(fingerprint)

    def _load_configs(self, path):
        configs = {}
        try:
            with open(path, 'r') as f:
                for line in f:
                    if "==>" not in line:
                         continue
                    name, args_str = line.split("==>")
                    args_dict = {}
                    for pair in args_str.split("|"):
                        k, v = pair.strip().split("=")
                        args_dict[k.strip()] = ast.literal_eval(v.strip())
                    configs[name.strip()] = args_dict
        except FileNotFoundError:
            print("Config not found, running without predefined args.")
        return configs


    def life_check(self, type='superficial', **kwargs):
        match type:
            case 'full':
                pass
                # ==> FOR FUTURE
                # check all the classes and their functions. try to launch esparate project in virtual environment.

            case 'superficial':
                pass
                # ==> FOR FUTURE
                # Every class has a 'check' function. For each class is different, but should be like checking the appearance of every other function.

            case 'specific':
                _class_names = kwargs.get('classes', [])
                _function_names = kwargs.get('functions', [])

                if _class_names is None or _function_names is None:
                    log.error
                # ==> FOR FUTURE
                # Check the output of specific function(s) in specific class(es)


    def _check_module(self, mod_name, instance):
        methods = inspect.getmembers(instance, predicate=inspect.ismethod)
        
        for method_name, method_ref in methods:
            if method_name.startswith("__"):
                continue
            
            # Берем аргументы из конфига или пустой словарь
            args = self.configs.get(method_name, {})
            
            try:
                # Если у метода есть параметр is_check, передаем его
                sig = inspect.signature(method_ref)
                if 'is_check' in sig.parameters:
                    args['is_check'] = True
                
                method_ref(**args)
                print(f"[OK] {mod_name}.{method_name}")
            except Exception as e:
                print(f"[BROKEN] {mod_name} module: '{method_name}()' failed: {e}")