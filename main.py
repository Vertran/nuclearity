import time
import os
import sys

import modules.instancer as instancer

#==== <MODULES> ====#
#===> [logger]
from modules.logger import Logger
Logger()

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


#===> [video manager]

#===> [audio manager]

#===> [multiplayer manager]


#==== <PRE-MAIN> ====#
field_nuclearity = filer.open_frames("data/other/fields.txt")
if field_nuclearity is None:
    log.warn('failed to load console label from file')
    log.info('main.py first log. Welcome to: NUCLEARITY', "main label not loaded")
else:
    log.info('main.py first log. Welcome to:\n', field_nuclearity[0], offset=0)


filer.open_style("data/styles/main_menu/menu.yaml")


#==== <MAIN> ====#
def main():
    log.info('Entering main loop')
    while True:
        uArgs = input('$> ')
        if uArgs == 'exit':
            break
        elif uArgs == 'reboot':
            os.execv(sys.executable, ['python'] + sys.argv)
        elif uArgs == 'clear logs':
            log.clear_logs()
        elif uArgs.split(' ')[0] == 'open':
            path = uArgs.split(' ')[1]
            content = filer.open_frames(path)
            if content is not None:
                for line in content:
                    print(line)
            else:
                log.warn(f"failed to open file: {path}")
            
        else:
            log.info(f"unknown command: {uArgs}")

main()

#==== <POST-MAIN> ====#
log.info('Exiting program.')

filer.kill()
log.kill()