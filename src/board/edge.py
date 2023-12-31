from dataclasses import dataclass
from typing import List

from src.board.mapping import edge_mapping


@dataclass
class Edge:
    def __init__(self, id):
        self.id = id
        self.nodes: List[int] = edge_mapping[self.id]["adjacent_nodes"]

    def near_nodes(self):
        return self.nodes
