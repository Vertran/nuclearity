import sys
import threading
import time

import modules.instancer as instancer

# ==== <MODULES> ====#
# ===> [logger]
from modules.logger import Logger

Logger()
assert instancer.log is not None

log = instancer.log


# ===> [life manager]
from modules.managers.life_manager import LifeManager

LifeManager()
assert instancer.managers["life"] is not None
life_manager = instancer.managers["life"]


# ===> [console manager]
from modules.managers.console_manager import Console

Console()
assert instancer.managers["console"] is not None
console_manager = instancer.managers["console"]


# ==> [object manager]
from modules.managers.object_manager import ObjectManager

ObjectManager()
assert instancer.managers["object"] is not None
object_manager = instancer.managers["object"]


# ===> [video manager]
from modules.managers.video_manager import VideoManager

VideoManager()
assert instancer.managers["video"] is not None
video_manager = instancer.managers["video"]


# ===> [audio manager]
from modules.managers.audio_manager import AudioManager

AudioManager()
assert instancer.managers["audio"] is not None
audio_manager = instancer.managers["audio"]


# ===> [internet manager]
from modules.managers.network_manager import NetworkManager

NetworkManager()
assert instancer.managers["network"] is not None
network_manager = instancer.managers["network"]


# ==== <LIFE-CHECK> ====#
# life_manager.life_check()


# ==== <PRE-MAIN> ====#
running = True


# ===> [functions]
def internet_main(argv):
    while running:
        uArg = input()

        if uArg == "exit":
            network_manager.disconnect()
            exit()
        else:
            try:
                network_manager.send({"type": "terminal_input", "message": uArg, "sender": f"Console-{argv[2]}"})
            except Exception as e:
                log.error('Network exception occured:', str(e))

# ==== <MAIN> ====#
def main():
    #argv = sys.argv

    time.sleep(2)
    try:
        log.info("Entering main loop")
        #threading.Thread(target=network_manager.connect, daemon=True).start()

        #threading.Thread(target=internet_main, args=[argv], daemon=True).start()

        video_manager.main()
    except Exception as e:
        log.error("CLIENT ERROR:", str(e))
        life_manager.fix_error(e)
        input("Error occurred. Press Enter to close...")


print("alala")
main()
input("Error occurred. Press Enter to close...")

# ==== <POST-MAIN> ====#
log.info("Exiting program.")

log.kill()
