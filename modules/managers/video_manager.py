import modules.instancer as instancer
log = instancer.log

class VideoManager:
    def __init__(self):
        log.info("Initializing Video Manager")
        self.screen = None
        self.clock = None
        

        instancer.managers["video"] = self
        log.info("Video Manager initialized successfully")

