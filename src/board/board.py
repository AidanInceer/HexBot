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
        return self.nodes[node_id - 1]

    def get_edge(self, edge_id: int) -> Edge:
        return self.edges[edge_id - 1]

    def get_harbor(self, harbor_id: int) -> Harbor:
        return self.harbors[harbor_id - 1]

    def active_tiles(self, roll: int) -> List[Tile]:
        return [tile for tile in self.tiles if tile.token == roll]

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

        board = f"""
        ==========================================================================
                                     X---------X
                                    /           \\
                                   /             \\
                        X---------X      {a}      X---------X
                       /           \\     ({a2})    /           \\
                      /             \\           /             \\
           X---------X      {d}      X---------X      {b}      X---------X
          /           \\     ({d2})    /           \\     ({b2})    /           \\
         /             \\           /             \\           /             \\
        X      {h}      X---------X      {e}      X---------X      {c}      X
         \\     ({h2})    /           \\     ({e2})    /           \\     ({c2})    /
          \\           /             \\           /             \\           /
           X---------X      {i}      X---------X      {f}      X---------X
          /           \\     ({i2})    /           \\     ({f2})    /           \\
         /             \\           /             \\           /             \\
        X      {m}      X---------X      {j}      X---------X      {g}      X
         \\     ({m2})    /           \\     ({j2})    /           \\     ({g2})    /
          \\           /             \\           /             \\           /
           X---------X      {n}      X---------X      {k}      X---------X
          /           \\     ({n2})    /           \\     ({k2})    /           \\
         /             \\           /             \\           /             \\
        X      {q}      X---------X      {o}      X---------X      {l}      X
         \\     ({q2})    /           \\     ({o2})    /           \\     ({l2})    /
          \\           /             \\           /             \\           /
           X---------X      {r}      X---------X      {p}      X---------X
                      \\     ({r2})    /           \\     ({p2})    /
                       \\           /             \\           /
                        X---------X      {s}      X---------X
                                   \\     ({s2})    /
                                    \\           /
                                     X---------X
        ==========================================================================
        """
        print(board)
