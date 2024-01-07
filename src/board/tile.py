from dataclasses import dataclass
from typing import List, Optional, Union

from src.board.mapping import tile_mapping
from src.board.terrain import Desert, Fields, Forest, Hills, Mountains, Pasture


@dataclass
class Tile:
    def __init__(self, type, id, robber=False):
        self.type: Union[Desert, Fields, Forest, Hills, Mountains, Pasture] = type
        self.id: int = id
        self.token: Union[None, int] = None
        self.nodes: List[int] = tile_mapping[self.id]["adjacent_nodes"]
        self.robber: bool = robber

    def __repr__(self) -> str:
        return f"Tile(name={self.type.name}, id={self.id}, token={self.token}, nodes={self.nodes})"

    def get_near_nodes(self):
        return self.nodes

    def tile(self):
        return self.type

    def value(self):
        return self.token

    def display_type(self):
        return self.type.name[:3].upper()

    def display_token(self):
        return "07" if self.token is None else str(self.token).zfill(2)

    def has_robber(self):
        return self.robber

    def display_id(self):
        return str(self.id).zfill(2)
