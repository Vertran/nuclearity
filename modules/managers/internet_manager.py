import modules.instancer as instancer
log = instancer.log

class InternetManager:
    def __init__(self):
        log.info("Initializing Internet Manager")
        self.connection = None
        self.status = "disconnected"
        
        instancer.managers["internet"] = self
        log.info("Internet Manager initialized successfully")