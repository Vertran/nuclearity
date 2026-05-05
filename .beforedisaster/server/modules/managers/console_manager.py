import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log


from modules.managers.submodules.buffers import Buffer


class Console:
    def __init__(self):
        log.info("Initializing console manager")

        # ==> sys
        self.mode = "sui"  # SimpleUI|NoUI|GraphicsUI
        self.commands = {}

        # ==> general
        self.dbuffer = Buffer("draw_buffer")
        self.cbuff = Buffer("command_buffer")

        # ==> finish
        instancer.managers["console"] = self
        log.info("Console manager initialized")

    def draw(self):
        pass
