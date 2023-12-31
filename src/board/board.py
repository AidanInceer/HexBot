import random
from dataclasses import dataclass
from typing import List, Optional

from .edge import Edge
from .harbor import Harbor
from .node import Node
from .terrain import Desert, Fields, Forest, Hills, Mountains, Pasture
from .tile import Tile


@dataclass
class Board:
    nodes: Optional[List[Node]] = None
    edges: Optional[List[Edge]] = None
    harbors: Optional[List[Harbor]] = None
    tiles: Optional[List[Tile]] = None

    def generate(self) -> None:
        # generate nodes, edges, harbors, tiles - obects are mapped and linked using
        # the mapping.py file and their internal init methods
        self.nodes = self.generate_nodes()
        self.edges = self.generate_edges()
        self.harbors = self.generate_harbors()
        self.tiles = self.generate_tiles()

    def generate_nodes(self):
        self.nodes = [Node(id=node_id + 1) for node_id in range(54)]
        return self.nodes

    def generate_edges(self):
        self.edges = [Edge(id=edge_id + 1) for edge_id in range(72)]
        return self.edges

    def generate_harbors(self):
        self.harbors = [
            Harbor(id=1, resource="all", rate=3),
            Harbor(id=2, resource="wheat", rate=2),
            Harbor(id=3, resource="ore", rate=2),
            Harbor(id=4, resource="lumber", rate=2),
            Harbor(id=5, resource="all", rate=3),
            Harbor(id=6, resource="brick", rate=2),
            Harbor(id=7, resource="wool", rate=2),
            Harbor(id=8, resource="all", rate=3),
            Harbor(id=9, resource="all", rate=3),
        ]

    def generate_tiles(self) -> List[Tile]:
        tile_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        random.shuffle(tile_ids)

        self.tiles = []
        # append Desert tiles
        for index in range(1):
            self.tiles.append(Tile(type=Desert(), id=tile_ids[index]))
            tile_ids[1:]

        # append Fields tiles
        for index in range(4):
            self.tiles.append(Tile(type=Fields(), id=tile_ids[index]))
            tile_ids[1:]

        # append Forest tiles
        for index in range(4):
            self.tiles.append(Tile(type=Forest(), id=tile_ids[index]))
            tile_ids[1:]

        # append Hills tiles
        for index in range(3):
            self.tiles.append(Tile(type=Hills(), id=tile_ids[index]))
            tile_ids[1:]

        # append Mountains tiles
        for index in range(3):
            self.tiles.append(Tile(type=Mountains(), id=tile_ids[index]))
            tile_ids[1:]

        # append Pasture tiles
        for index in range(4):
            self.tiles.append(Tile(type=Pasture(), id=tile_ids[index]))
            tile_ids[1:]

        self.apply_tokens()
        return self.tiles

    def apply_tokens(self):
        tokens = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        for tile in self.tiles:
            if isinstance(tile.type, Desert):
                tile.token = None
            else:
                tile.token = random.choice(tokens)
                tokens.remove(tile.token)
        return self.tiles

    def link_nodes_to_nodes(self, node_mapping: dict[str, List[int]]):
        for node in self.nodes:
            node.add_near_nodes(node_mapping)

    def link_nodes_to_edges(self, node_mapping: dict[str, List[int]]):
        for node in self.nodes:
            node.add_near_edges(node_mapping)

    def link_nodes_to_harbors(self, node_mapping: dict[str, List[int]]):
        for node in self.nodes:
            node.add_near_harbors(node_mapping)

    def link_nodes_to_tiles(self, node_mapping: dict[str, List[int]]):
        for node in self.nodes:
            node.add_near_tiles(node_mapping)

    def link_edges_to_nodes(self, edge_mapping: dict[str, List[int]]):
        for edge in self.edges:
            edge.add_near_nodes(edge_mapping)

    def link_harbors_to_nodes(self, harbor_mapping: dict[str, List[int]]):
        for harbor in self.harbors:
            harbor.add_near_nodes(harbor_mapping)

    def link_tiles_to_nodes(self, tile_mapping: dict[str, List[int]]):
        for tile in self.tiles:
            tile.add_near_nodes(tile_mapping)
