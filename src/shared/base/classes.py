from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NucEvent:
    name:           str
    level:          str
    caller:         str
    timestamp:      str
    description:    str = ''

    def __str__(self):
        return f"[EVENT] [{self.timestamp}] [{self.level:^8}] [{self.caller:^12}] [{self.name:^12}] >> {self.description}"


@dataclass(frozen=True)
class NucLog:
    level:          str
    module:         str
    message:        str
    timestamp:      str
    description:    str = ''

    def __str__(self):
        return f"[ LOG ] [{self.timestamp}] [{self.level:^8}] [{self.module:^12}] >> {self.message}\n\t{self.description}"