from dataclasses import dataclass
from typing import List, Union

from src.board.mapping import node_mapping
from src.build.buildings import City, Settlement


@dataclass
class Node:
    def __init__(self, id):
        self.id: int = id
        self.nodes: List[int] = node_mapping[self.id]["adjacent_nodes"]
        self.edges: List[int] = node_mapping[self.id]["adjacent_edges"]
        self.harbors: List[int] = node_mapping[self.id]["adjacent_harbor"]
        self.tiles: List[int] = node_mapping[self.id]["adjacent_tiles"]
        self.occupied: bool = False
        self.building: Union[None, Settlement, City] = None
        self.color: Union[None, str] = None

    def near_nodes(self):
        return self.nodes

    def near_edges(self):
        return self.edges

    def near_harbors(self):
        return self.harbors

    def near_tiles(self):
        return self.tiles
