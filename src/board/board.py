from __future__ import annotations

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

    def set_robber_tile(self, selected_tile: Tile) -> Tile:
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
            Harbor(id=i, resource=res, rate=rate)
            for i, (res, rate) in enumerate(
                [
                    ("all", 3),
                    ("wheat", 2),
                    ("ore", 2),
                    ("wood", 2),
                    ("all", 3),
                    ("brick", 2),
                    ("sheep", 2),
                    ("all", 3),
                    ("all", 3),
                ]
            )
        ]
        return self.harbors

    def generate_tiles(self) -> List[Tile]:
        tile_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        random.shuffle(tile_ids)

        tile_types = (
            [Desert()]
            + [Fields()] * 4
            + [Forest()] * 4
            + [Pasture()] * 4
            + [Mountains()] * 3
            + [Hills()] * 3
        )
        self.tiles = [
            Tile(type=tile_type, id=tile_id)
            for tile_type, tile_id in zip(tile_types, tile_ids)
        ]
        self.tiles[0].robber = True

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
        n = []
        for i in range(54):
            n.append(self.nodes[i].display_node())
        (
            n00,
            n01,
            n02,
            n03,
            n04,
            n05,
            n06,
            n07,
            n08,
            n09,
            n10,
            n11,
            n12,
            n13,
            n14,
            n15,
            n16,
            n17,
            n18,
            n19,
            n20,
            n21,
            n22,
            n23,
            n24,
            n25,
            n26,
            n27,
            n28,
            n29,
            n30,
            n31,
            n32,
            n33,
            n34,
            n35,
            n36,
            n37,
            n38,
            n39,
            n40,
            n41,
            n42,
            n43,
            n44,
            n45,
            n46,
            n47,
            n48,
            n49,
            n50,
            n51,
            n52,
            n53,
        ) = n

        e = []
        for i in range(72):
            e.append(self.edges[i].display_edge())
        (
            e00,
            e01,
            e02,
            e03,
            e04,
            e05,
            e06,
            e07,
            e08,
            e09,
            e10,
            e11,
            e12,
            e13,
            e14,
            e15,
            e16,
            e17,
            e18,
            e19,
            e20,
            e21,
            e22,
            e23,
            e24,
            e25,
            e26,
            e27,
            e28,
            e29,
            e30,
            e31,
            e32,
            e33,
            e34,
            e35,
            e36,
            e37,
            e38,
            e39,
            e40,
            e41,
            e42,
            e43,
            e44,
            e45,
            e46,
            e47,
            e48,
            e49,
            e50,
            e51,
            e52,
            e53,
            e54,
            e55,
            e56,
            e57,
            e58,
            e59,
            e60,
            e61,
            e62,
            e63,
            e64,
            e65,
            e66,
            e67,
            e68,
            e69,
            e70,
            e71,
        ) = e

        i_values = []
        t_values = []
        p_values = []

        for i in range(19):
            i_values.append(self.tiles[i].display_token())
            t_values.append(self.tiles[i].display_type())
            p_values.append(self.tiles[i].display_pips())

        (
            i00,
            i01,
            i02,
            i03,
            i04,
            i05,
            i06,
            i07,
            i08,
            i09,
            i10,
            i11,
            i12,
            i13,
            i14,
            i15,
            i16,
            i17,
            i18,
        ) = i_values
        (
            t00,
            t01,
            t02,
            t03,
            t04,
            t05,
            t06,
            t07,
            t08,
            t09,
            t10,
            t11,
            t12,
            t13,
            t14,
            t15,
            t16,
            t17,
            t18,
        ) = t_values
        (
            p00,
            p01,
            p02,
            p03,
            p04,
            p05,
            p06,
            p07,
            p08,
            p09,
            p10,
            p11,
            p12,
            p13,
            p14,
            p15,
            p16,
            p17,
            p18,
        ) = p_values

        h_values = [self.harbors[i].display_harbor() for i in range(9)]
        h00, h01, h02, h03, h04, h05, h06, h07, h08 = h_values

        board = f"""
===========================================================================================

                                                     {h00}
                                                         ||
                                                   {n00}--{e00}--{n01}
                                                  /              \\
                                                 {e06}               {e01}
                                                /        {i00}        \\
                                   {n07}--{e10}--{n08}     {t00}    {n02}--{e02}--{n03}
                                  /              \\      {p00}     /              \\
                  {h03}- - -{e18}               {e11}             {e07}               {e03}- - -{h01}
                                /        {i03}        \\            /        {i01}        \\
                   {n16}--{e23}--{n17}     {t03}    {n09}--{e12}--{n10}     {t01}    {n04}--{e04}--{n05}
                  /              \\      {p03}     /              \\      {p01}     /              \\
                 {e33}               {e24}             {e19}               {e13}             {e08}               {e05}
                /        {i07}        \\            /        {i04}        \\            /        {i02}        \\
             {n27}     {t07}    {n18}--{e25}--{n19}     {t04}    {n11}--{e14}--{n12}     {t02}    {n06}
                 \\      {p07}     /              \\      {p04}     /              \\      {p02}     /
                  {e39}             {e34}               {e26}             {e20}               {e15}             {e09}
                   \\            /        {i08}        \\            /        {i05}        \\            /
                   {n28}--{e40}--{n29}     {t08}    {n20}--{e27}--{n21}     {t05}    {n13}--{e16}--{n14}
                  /              \\      {p08}     /              \\      {p05}     /              \\
 {h05}- - -{e49}               {e41}             {e35}               {e28}             {e21}               {e17}- - -{h02}
                /        {i12}        \\            /        {i09}        \\            /        {i06}        \\
             {n38}     {t12}    {n30}--{e42}--{n31}     {t09}    {n22}--{e29}--{n23}     {t06}    {n15}
                 \\      {p12}     /              \\      {p09}     /              \\      {p06}     /
                  {e54}             {e50}               {e43}             {e36}               {e30}             {e22}
                   \\            /        {i13}        \\            /        {i10}        \\            /
                   {n39}--{e55}--{n40}     {t13}    {n32}--{e44}--{n33}     {t10}    {n24}--{e31}--{n25}
                  /              \\      {p13}     /              \\      {p10}     /              \\
                 {e62}               {e56}             {e51}               {e45}             {e37}               {e32}
                /        {i16}        \\            /        {i14}        \\            /        {i11}        \\
             {n47}     {t16}    {n41}--{e57}--{n42}     {t14}    {n34}--{e46}--{n35}     {t11}    {n26}
                 \\      {p16}     /              \\      {p14}     /              \\      {p11}     /
    {h07}- - -{e66}             {e63}               {e58}             {e52}               {e47}             {e38}- - -{h04}
                   \\            /        {i17}        \\            /        {i15}        \\            /
                   {n48}--{e67}--{n49}     {t17}    {n43}--{e59}--{n44}     {t15}    {n36}--{e48}--{n37}
                                 \\      {p17}     /              \\      {p15}     /
                                  {e68}             {e64}               {e60}             {e53}
                                   \\            /        {i18}        \\            /
                                   {n50}--{e69}--{n51}     {t18}    {n45}--{e61}--{n46}
                                                 \\      {p18}     /      ||
                                    {h08}- - -{e70}             {e65}   {h06}
                                                   \\            /
                                                   {n52}--{e71}--{n53}

==========================================================================================="""
        print(board)
