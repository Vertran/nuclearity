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
from modules.managers.internet_manager import InternetManager
InternetManager()
assert instancer.managers['internet'] is not None
internet_manager = instancer.managers['internet']

#==== <PRE-MAIN> ====#
field_nuclearity = filer.open_frames("data/other/fields.txt")
if field_nuclearity is None:
    log.warn('failed to load console label from file')
    log.info('main.py first log. Welcome to: NUCLEARITY', "main label not loaded")
else:
    log.info('main.py first log. Welcome to:\n', field_nuclearity[0], offset=0)


filer.open_style("data/styles/main_menu/menu.yaml")




#===> [functions]

def cat_file():
    path = input('$ Path> ').replace('[A', '').replace('[B', '').replace('[C', '').replace('[D', '')
    print(path)
    content = filer.open_frames(path)
    if content is not None:
        for line in content:
            print(line)

        print()
    else:
        log.warn(f"failed to open file: `{path}`")

def console_ui():
    from colorama import Fore, Back, Style, init

    init()


    run = True
    selected_id = 0

    commands = [
        {
            "display":"start",
            "hint":"Starts the game",
            "is_active": True,
            "function": print
        },
        {
            "display":"open",
            "hint":"Opens file. <path/to/file>",
            "is_active": False,
            "function": cat_file
        },
        {
            "display":"reboot",
            "hint":"Reboots the console",
            "is_active": False,
            "function": print
        },
        {
            "display":"exit",
            "hint":"Exits the console",
            "is_active": False,
            "function": exit
        }
    ]

    

    print('Welkome to the NUCLEARITY console. Here are aviable commands at the moment:')

    print("\n\n\n\n")
    print('\033[5F')

    for command in commands:            
        if command['is_active']:
            print('>', command['display'] + f" -- {command['hint']}\033[K")
        else:
            print(' ', f"{command['display']}\033[K")

    while run:
        if glfw.get_key(video_manager.window, glfw.KEY_UP) == glfw.PRESS:
            if selected_id == 0:
                selected_id = len(commands) - 1
                commands[0]['is_active'] = False
            
            else:
                selected_id -= 1
                commands[selected_id + 1]['is_active'] = False
            
            commands[selected_id]['is_active'] = True


            print('\033[5F')

            for command in commands:            
                if command['is_active']:
                    print('>', command['display'] + f" -- {command['hint']}\033[K")
                else:
                    print(' ', f"{command['display']}\033[K")


        elif glfw.get_key(video_manager.window, glfw.KEY_DOWN) == glfw.PRESS:
            if selected_id == len(commands) - 1:
                selected_id = 0
                commands[len(commands) - 1]['is_active'] = False
            else:
                selected_id += 1
                commands[selected_id - 1]['is_active'] = False

            commands[selected_id]['is_active'] = True

            print('\033[5F')

            for command in commands:            
                if command['is_active']:
                    print('>', command['display'] + f" -- {command['hint']}\033[K")
                else:
                    print(' ', f"{command['display']}\033[K")



        elif glfw.get_key(video_manager.window, glfw.KEY_ENTER) == glfw.PRESS:
            commands[selected_id]['function']()

        time.sleep(0.01)
    
    
    
    #print(': start -- Starts the game.')
    #print(': open <path/to/file> -- prints this file in console.')
    #print(': ')
    #print(': reboot -- reboots the console.')
    #print(': exit -- exits this console.')


#==== <MAIN> ====#
def main():
    video_manager.main()
    console_ui()
    log.info('Entering main loop')
    while True:
        uArgs = input('$> ')
        log.info(f"User input: `{uArgs}`")
        if uArgs == 'exit':
            break
        elif uArgs == 'reboot':
            os.execv(sys.executable, ['python'] + sys.argv)
        elif uArgs == 'help':
            print("Available commands:")
            print("- exit: Exit the program")
            print("- reboot: Reboot the program")
            print("- clear logs: Clear the log file")
            print("- open <path>: Open a file and display its contents")
        elif uArgs == 'clear logs':
            log.clear_logs()
        elif uArgs.split(' ')[0] == 'open':
            path = uArgs.split(' ')[1]
            content = filer.open_frames(path)
            if content is not None:
                for line in content:
                    print(line)
            else:
                log.warn(f"failed to open file: `{path}`")
            
        else:
            log.info(f"unknown command: `{uArgs}`")

main()

#==== <POST-MAIN> ====#
log.info('Exiting program.')

filer.kill()
log.kill()
