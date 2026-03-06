import time

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



#===> [console manager]
from modules.managers.console_manager import Console
Console()
assert instancer.managers['console'] is not None
console_manager = instancer.managers['console']

#===> [internet manager]
from modules.managers.network_manager import NetworkManager
NetworkManager()
assert instancer.managers['network'] is not None
network_manager = instancer.managers['network']



#===> [functions]


#==== <MAIN> ====#
def main():
    log.info('Entering main loop')



main()

#==== <POST-MAIN> ====#
log.info('Exiting program.')

log.kill()
