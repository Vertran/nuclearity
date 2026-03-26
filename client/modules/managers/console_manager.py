import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log

import sys

from modules.managers.submodules.buffers import Buffer


class Console:
    @instancer.manager
    def __init__(self):

        #==> sys
        self.mode = 'sui' #SimpleUI|NoUI|GraphicsUI
        self.commands = {}

        #==> general
        self.dbuffer = Buffer('draw_buffer')
        self.cbuff = Buffer('command_buffer')

        #==> finish
        instancer.managers["console"] = self

    def draw(self):
        pass