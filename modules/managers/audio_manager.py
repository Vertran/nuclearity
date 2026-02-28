import modules.instancer as instancer
log = instancer.log

class AudioManager:
    def __init__(self):
        log.info("Initializing Audio Manager")
        self.audio_system = None
        self.volume = 100
        
        instancer.managers["audio"] = self
        log.info("Audio Manager initialized successfully")