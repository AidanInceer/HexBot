from dataclasses import dataclass
from typing import List, Union

from src.board.mapping import tile_mapping
from src.board.terrain import Desert, Fields, Forest, Hills, Mountains, Pasture


@dataclass
class Tile:
    def __init__(self, type, id):
        self.type: Union[Desert, Fields, Forest, Hills, Mountains, Pasture] = type
        self.id: int = id
        self.token: Union[None, int] = None
        self.nodes: List[int] = tile_mapping[self.id]["adjacent_nodes"]

    def near_nodes(self):
        return self.nodes

    def tile(self):
        return self.type

    def value(self):
        return self.token
