from dataclasses import dataclass
from typing import List

from src.catan.board.mapping import harbor_mapping


@dataclass
class Harbor:
    def __init__(self, id: int, resource: str, rate: int):
        self.id: int = id
        self.resource: str = resource
        self.rate: int = rate
        self.nodes: List[int] = harbor_mapping[self.id]["adjacent_nodes"]

    def near_nodes(self) -> List[int]:
        return self.nodes

    def type(self) -> str:
        return self.resource

    def trade_rate(self) -> int:
        return self.rate

    def display_harbor(self) -> str:
        return f"[{self.resource} {self.rate}:1]"
