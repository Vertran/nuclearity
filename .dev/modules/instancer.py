from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.logger import Logger

log: "Logger | None" = None
