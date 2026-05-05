import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log

assert instancer.event_bus is not None
event_bus = instancer.event_bus

class AudioManager:
    @instancer.manager
    def __init__(self):
        log.info("Initializing Audio Manager")
        self.audio_system = None
        self.volume = 100
        
        log.info("Audio Manager initialized successfully")