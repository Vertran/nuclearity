import modules.instancer as instancer

# ==== <MODULES> ====#
# ===> [logger]
from modules.logger import Logger

Logger()
assert instancer.log is not None

log = instancer.log

from modules.managers.game_manager import GameManager
GameManager()

assert instancer.managers['game'] is not None
gm = instancer.managers['game']

gm.init()


# ==== <PRE-MAIN> ====#
running = True


# ==== <MAIN> ====#
def main():
    try:
        pass
    except Exception as e:
        log.error("CLIENT ERROR:", str(e))
        input("Error occurred. Press Enter to close...")


main()

# ==== <POST-MAIN> ====#
log.info("Exiting program.")

log.kill()
