from dataclasses import dataclass, field
from typing import List


@dataclass
class Settlement:
    color: str
    id: int


@dataclass
class City:
    color: str
    id: int


@dataclass
class Road:
    color: str
    id: int


@dataclass
class Buildings:
    settlements: List[Settlement] = field(default_factory=list)
    cities: List[City] = field(default_factory=list)
    roads: List[Road] = field(default_factory=list)
