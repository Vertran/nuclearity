from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.filer import Filer
    from modules.logger import Logger

log: "Logger | None" = None
filer: "Filer | None" = None

managers: dict = {
    "video": None,
    "audio": None,
    "internet": None,
    "console": None,
}

state: dict = {
    "running": True,
    "drawing": True,
}