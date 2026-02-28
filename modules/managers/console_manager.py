import modules.instancer as instancer
log = instancer.log

import sys

from modules.managers.submodules.buffers import Buffer

def save(args):
    path = args[0]
    data = args[1]
    result = filer.save_style(path, data)
    if result:
        log.info(f"file saved successfully: {path}")
    else:
        log.warn(f"failed to save file: {path}")

class Console:
    def __init__(self):
        log.info("Initializing console manager")

        #==> sys
        self.mode = 'sui' #SimpleUI|NoUI
        self.commands = {}

        #==> general
        self.dbuffer = Buffer('draw_buffer')
        self.cbuff = Buffer('command_buffer')

        #==> finish
        instancer.managers["console"] = self
        log.info("Console manager initialized")

    def draw():
        pass