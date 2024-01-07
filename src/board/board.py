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

    def get_node(self, node_id: int) -> Node:
        return self.nodes[node_id]

    def get_edge(self, edge_id: int) -> Edge:
        return self.edges[edge_id]

    def get_harbor(self, harbor_id: int) -> Harbor:
        return self.harbors[harbor_id]

    def active_tiles(self, roll: int) -> List[Tile]:
        return [tile for tile in self.tiles if tile.token == roll]

    def set_robber_tile(self, selected_tile) -> Tile:
        for tile in self.tiles:
            if tile.id == selected_tile:
                return tile

    def get_robber_tile(self) -> Tile:
        for tile in self.tiles:
            if tile.robber:
                return tile

    def generate(self) -> None:
        # generate nodes, edges, harbors, tiles - obects are mapped and linked using
        # the mapping.py file and their internal init methods
        self.nodes = self.generate_nodes()
        self.edges = self.generate_edges()
        self.harbors = self.generate_harbors()
        self.tiles = self.generate_tiles()

    def generate_nodes(self):
        self.nodes = [Node(id=node_id) for node_id in range(54)]
        return self.nodes

    def generate_edges(self):
        self.edges = [Edge(id=edge_id) for edge_id in range(72)]
        return self.edges

    def generate_harbors(self):
        self.harbors = [
            Harbor(id=0, resource="all", rate=3),
            Harbor(id=1, resource="wheat", rate=2),
            Harbor(id=2, resource="ore", rate=2),
            Harbor(id=3, resource="wood", rate=2),
            Harbor(id=4, resource="all", rate=3),
            Harbor(id=5, resource="brick", rate=2),
            Harbor(id=6, resource="sheep", rate=2),
            Harbor(id=7, resource="all", rate=3),
            Harbor(id=8, resource="all", rate=3),
        ]
        return self.harbors

    def generate_tiles(self) -> List[Tile]:
        tile_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        random.shuffle(tile_ids)

        self.tiles = [
            Tile(type=Desert(), robber=True, id=tile_ids[0]),
            Tile(type=Fields(), id=tile_ids[1]),
            Tile(type=Fields(), id=tile_ids[2]),
            Tile(type=Fields(), id=tile_ids[3]),
            Tile(type=Fields(), id=tile_ids[4]),
            Tile(type=Forest(), id=tile_ids[5]),
            Tile(type=Forest(), id=tile_ids[6]),
            Tile(type=Forest(), id=tile_ids[7]),
            Tile(type=Forest(), id=tile_ids[8]),
            Tile(type=Pasture(), id=tile_ids[9]),
            Tile(type=Pasture(), id=tile_ids[10]),
            Tile(type=Pasture(), id=tile_ids[11]),
            Tile(type=Pasture(), id=tile_ids[12]),
            Tile(type=Mountains(), id=tile_ids[13]),
            Tile(type=Mountains(), id=tile_ids[14]),
            Tile(type=Mountains(), id=tile_ids[15]),
            Tile(type=Hills(), id=tile_ids[16]),
            Tile(type=Hills(), id=tile_ids[17]),
            Tile(type=Hills(), id=tile_ids[18]),
        ]

        random.shuffle(self.tiles)
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

    def display(self) -> None:
        a, a2 = self.tiles[0].display_type(), self.tiles[0].display_token()
        b, b2 = self.tiles[1].display_type(), self.tiles[1].display_token()
        c, c2 = self.tiles[2].display_type(), self.tiles[2].display_token()
        d, d2 = self.tiles[3].display_type(), self.tiles[3].display_token()
        e, e2 = self.tiles[4].display_type(), self.tiles[4].display_token()
        f, f2 = self.tiles[5].display_type(), self.tiles[5].display_token()
        g, g2 = self.tiles[6].display_type(), self.tiles[6].display_token()
        h, h2 = self.tiles[7].display_type(), self.tiles[7].display_token()
        i, i2 = self.tiles[8].display_type(), self.tiles[8].display_token()
        j, j2 = self.tiles[9].display_type(), self.tiles[9].display_token()
        k, k2 = self.tiles[10].display_type(), self.tiles[10].display_token()
        l, l2 = self.tiles[11].display_type(), self.tiles[11].display_token()
        m, m2 = self.tiles[12].display_type(), self.tiles[12].display_token()
        n, n2 = self.tiles[13].display_type(), self.tiles[13].display_token()
        o, o2 = self.tiles[14].display_type(), self.tiles[14].display_token()
        p, p2 = self.tiles[15].display_type(), self.tiles[15].display_token()
        q, q2 = self.tiles[16].display_type(), self.tiles[16].display_token()
        r, r2 = self.tiles[17].display_type(), self.tiles[17].display_token()
        s, s2 = self.tiles[18].display_type(), self.tiles[18].display_token()

        n0 = "00"
        e0 = "01"
        t0 = "02"
        i0 = "03"
        p0 = "04"

        board = f"""
===========================================================================================
                                                   ({n0})--{e0}--({n0})
                                                  /              \\
                                                 {e0}               {e0}
                                                /        {i0}        \\
                                   ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})
                                  /              \\       {p0}       /              \\
                                 {e0}               {e0}             {e0}               {e0}
                                /        {i0}        \\            /        {i0}        \\
                   ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})
                  /              \\       {p0}       /              \\       {p0}       /              \\
                 {e0}               {e0}             {e0}               {e0}             {e0}               {e0}
                /        {i0}        \\            /        {i0}        \\            /        {i0}        \\
             ({n0})        {t0}        ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})        {t0}        ({n0})
                 \\       {p0}       /              \\       {p0}       /              \\       {p0}       /
                  {e0}             {e0}               {e0}             {e0}               {e0}             {e0}
                   \\            /        {i0}        \\            /        {i0}        \\            /
                   ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})
                  /              \\       {p0}       /              \\       {p0}       /              \\
                 {e0}               {e0}             {e0}               {e0}             {e0}               {e0}
                /        {i0}        \\            /        {i0}        \\            /        {i0}        \\
             ({n0})        {t0}        ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})        {t0}        ({n0})
                 \\       {p0}       /              \\       {p0}       /              \\       {p0}       /
                  {e0}             {e0}               {e0}             {e0}               {e0}             {e0}
                   \\            /        {i0}        \\            /        {i0}        \\            /
                   ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})
                  /              \\       {p0}       /              \\       {p0}       /              \\
                 {e0}               {e0}             {e0}               {e0}             {e0}               {e0}
                /        {i0}        \\            /        {i0}        \\            /        {i0}        \\
             ({n0})        {t0}        ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})        {t0}        ({n0})
                 \\       {p0}       /              \\       {p0}       /              \\       {p0}       /
                  {e0}             {e0}               {e0}             {e0}               {e0}             {e0}
                   \\            /        {i0}        \\            /        {i0}        \\            /
                   ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})
                                 \\       {p0}       /              \\       {p0}       /
                                  {e0}             {e0}               {e0}             {e0}
                                   \\            /        {i0}        \\            /
                                   ({n0})--{e0}--({n0})        {t0}        ({n0})--{e0}--({n0})
                                                 \\       {p0}       /
                                                  {e0}             {e0}
                                                   \\            /
                                                   ({n0})--{e0}--({n0})

==========================================================================================="""
        print(board)
