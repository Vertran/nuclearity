from dataclasses import dataclass, field
from typing import Any


@dataclass
class Assign:
    target: str
    value: Any

@dataclass
class BinOp:
    op: str
    left: Any
    right: Any

@dataclass
class If:
    condition: Any
    body: list

@dataclass
class Name:
    value: str

@dataclass
class Literal:
    value: Any

@dataclass
class Call:
    func: str
    args: list

@dataclass
class While:
    condition: Any
    body: list

@dataclass
class Each:
    var: str
    iterable: Any
    body: list