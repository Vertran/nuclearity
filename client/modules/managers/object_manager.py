import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log

import yaml
from modules.instancer import OBJECT
from modules.managers.submodules.objects import *


class ObjectManager:
    def __init__(self):
        log.info("Initializing Object Manager")

        self.draw_objects = []
        self.update_objects = []

        self.styles =  {}

        instancer.managers["object"] = self
        log.info("Object Manager initialized successfully")

    def create_from_file(self, path):
        objs_d_tmp = []
        objs_u_tmp = []
        updatable = False
        with open(path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            menu_tree = data['structure']

        self.styles = data.get('styles', {})

        #log.debug('\n', menu_tree)

        for object in menu_tree:
            try:

                props = object.get('properties', {})
                raw_type = props.get('type', 'rect')

                
                base = self.styles.get(props.pop('extends'), {})
                object['properties'] = {**base, **props}
                match raw_type:
                    case 'circle':
                        obj = RegularPolygon(**props)
                        updatable = False

                    case 'rect':
                        obj = Rect(**props)
                        updatable = False

                    case 'line':
                        obj = Line(**props)
                        updatable = False

                    case 'button':
                        obj = Button(**props)
                        updatable = True

                    case 'input_field':
                        obj = InputField(**props)
                        updatable = True

                    #case 'label':
                    #    obj = Label(**props)
                    #    updatable = False

                    #case 'text-field':
                    #    obj = TextField(**props)
                    #    updatable = True


                    case _:
                        log.warn(f'No shape found for `{raw_type}`',**props)
                        continue

                objs_d_tmp.append(obj)
                if updatable:
                    objs_u_tmp.append(obj)
                log.info(f'Object created: {raw_type}')
            except Exception as e:
                log.error('An Exception Occured while creating the object:', str(e))

        self.draw_objects.clear()
        self.draw_objects.extend(objs_d_tmp)
        self.update_objects.clear()
        self.update_objects.extend(objs_u_tmp)

        log.info('Updated the draw buffer')        



    def get_objects(self):
        #for obj in self.draw_objects:
        #    print(f"draw__{obj.name}; {obj.x, obj.y}")

        #for obj in self.update_objects:
        #    print(f"update__{obj.name}; {obj.x, obj.y}")

        return [self.draw_objects, self.update_objects]