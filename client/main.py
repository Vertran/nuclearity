import time
import os
import sys
import glfw

import modules.instancer as instancer

#==== <MODULES> ====#
#===> [logger]
from modules.logger import Logger
Logger()
assert instancer.log is not None

log = instancer.log
i = 0
while log is None:
    if i > 3:
        print('[ERROR] logger not initialized')
        exit()
    
    print(f'[WARN] {i} waiting for logger initialization...')
    i += 1
    time.sleep(0.5)


#===> [filer]
from modules.filer import Filer
Filer()
assert instancer.filer is not None

filer = instancer.filer
i = 0
while filer is None:
    
    if i > 3:
        log.error('filer not initialized')
        log.kill()
        exit()

    log.warn(f'{i} waiting for filer initialization...')
    i += 1
    time.sleep(0.5)


#===> [console manager]
from modules.managers.console_manager import Console
Console()
assert instancer.managers['console'] is not None
console_manager = instancer.managers['console']

#==> [object manager]
from modules.managers.object_manager import ObjectManager
ObjectManager()
assert instancer.managers['object'] is not None
object_manager = instancer.managers['object']

#===> [video manager]
from modules.managers.video_manager import VideoManager
VideoManager()
assert instancer.managers['video'] is not None
video_manager = instancer.managers['video']

#===> [audio manager]
from modules.managers.audio_manager import AudioManager
AudioManager()
assert instancer.managers['audio'] is not None
audio_manager = instancer.managers['audio']

#===> [internet manager]
from modules.managers.network_manager import NetworkManager
NetworkManager()
assert instancer.managers['network'] is not None
network_manager = instancer.managers['network']

#==== <PRE-MAIN> ====#
field_nuclearity = filer.open_frames("data/other/fields.txt")
if field_nuclearity is None:
    log.warn('failed to load console label from file')
    log.info('main.py first log. Welcome to: NUCLEARITY', "main label not loaded")
else:
    log.info('main.py first log. Welcome to:\n', field_nuclearity[0], offset=0)


#===> [functions]


#==== <MAIN> ====#
def main():
    log.info('Entering main loop')
    video_manager.main()


main()

#==== <POST-MAIN> ====#
log.info('Exiting program.')

filer.kill()
log.kill()
