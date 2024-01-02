from dataclasses import dataclass
from typing import List, Union

from src.board.mapping import edge_mapping, node_mapping


@dataclass
class Edge:
    def __init__(self, id):
        self.id = id
        self.nodes: List[int] = edge_mapping[self.id]["adjacent_nodes"]
        self.edges: List[int] = edge_mapping[self.id]["adjacent_edges"]
        self.occupied: bool = False
        self.color: Union[None, str] = None

    def near_nodes(self):
        return self.nodes
