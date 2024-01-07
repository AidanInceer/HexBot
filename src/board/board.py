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
        n00 = self.nodes[0].display_node()
        n01 = self.nodes[1].display_node()

        n02 = self.nodes[2].display_node()

        n03 = self.nodes[3].display_node()
        n04 = self.nodes[4].display_node()
        n05 = self.nodes[5].display_node()
        n06 = self.nodes[6].display_node()
        n07 = self.nodes[7].display_node()
        n08 = self.nodes[8].display_node()
        n09 = self.nodes[9].display_node()
        n10 = self.nodes[10].display_node()
        n11 = self.nodes[11].display_node()
        n12 = self.nodes[12].display_node()
        n13 = self.nodes[13].display_node()
        n14 = self.nodes[14].display_node()
        n15 = self.nodes[15].display_node()
        n16 = self.nodes[16].display_node()
        n17 = self.nodes[17].display_node()
        n18 = self.nodes[18].display_node()
        n19 = self.nodes[19].display_node()
        n20 = self.nodes[20].display_node()
        n21 = self.nodes[21].display_node()
        n22 = self.nodes[22].display_node()
        n23 = self.nodes[23].display_node()
        n24 = self.nodes[24].display_node()
        n25 = self.nodes[25].display_node()
        n26 = self.nodes[26].display_node()
        n27 = self.nodes[27].display_node()
        n28 = self.nodes[28].display_node()
        n29 = self.nodes[29].display_node()
        n30 = self.nodes[30].display_node()
        n31 = self.nodes[31].display_node()
        n32 = self.nodes[32].display_node()
        n33 = self.nodes[33].display_node()
        n34 = self.nodes[34].display_node()
        n35 = self.nodes[35].display_node()
        n36 = self.nodes[36].display_node()
        n37 = self.nodes[37].display_node()
        n38 = self.nodes[38].display_node()
        n39 = self.nodes[39].display_node()
        n40 = self.nodes[40].display_node()
        n41 = self.nodes[41].display_node()
        n42 = self.nodes[42].display_node()
        n43 = self.nodes[43].display_node()
        n44 = self.nodes[44].display_node()
        n45 = self.nodes[45].display_node()
        n46 = self.nodes[46].display_node()
        n47 = self.nodes[47].display_node()
        n48 = self.nodes[48].display_node()
        n49 = self.nodes[49].display_node()
        n50 = self.nodes[50].display_node()
        n51 = self.nodes[51].display_node()
        n52 = self.nodes[52].display_node()
        n53 = self.nodes[53].display_node()

        e00 = self.edges[0].display_edge()
        e01 = self.edges[1].display_edge()
        e02 = self.edges[2].display_edge()
        e03 = self.edges[3].display_edge()
        e04 = self.edges[4].display_edge()
        e05 = self.edges[5].display_edge()
        e06 = self.edges[6].display_edge()
        e07 = self.edges[7].display_edge()
        e08 = self.edges[8].display_edge()
        e09 = self.edges[9].display_edge()
        e10 = self.edges[10].display_edge()
        e11 = self.edges[11].display_edge()
        e12 = self.edges[12].display_edge()
        e13 = self.edges[13].display_edge()
        e14 = self.edges[14].display_edge()
        e15 = self.edges[15].display_edge()
        e16 = self.edges[16].display_edge()
        e17 = self.edges[17].display_edge()
        e18 = self.edges[18].display_edge()
        e19 = self.edges[19].display_edge()
        e20 = self.edges[20].display_edge()
        e21 = self.edges[21].display_edge()
        e22 = self.edges[22].display_edge()
        e23 = self.edges[23].display_edge()
        e24 = self.edges[24].display_edge()
        e25 = self.edges[25].display_edge()
        e26 = self.edges[26].display_edge()
        e27 = self.edges[27].display_edge()
        e28 = self.edges[28].display_edge()
        e29 = self.edges[29].display_edge()
        e30 = self.edges[30].display_edge()
        e31 = self.edges[31].display_edge()
        e32 = self.edges[32].display_edge()
        e33 = self.edges[33].display_edge()
        e34 = self.edges[34].display_edge()
        e35 = self.edges[35].display_edge()
        e36 = self.edges[36].display_edge()
        e37 = self.edges[37].display_edge()
        e38 = self.edges[38].display_edge()
        e39 = self.edges[39].display_edge()
        e40 = self.edges[40].display_edge()
        e41 = self.edges[41].display_edge()
        e42 = self.edges[42].display_edge()
        e43 = self.edges[43].display_edge()
        e44 = self.edges[44].display_edge()
        e45 = self.edges[45].display_edge()
        e46 = self.edges[46].display_edge()
        e47 = self.edges[47].display_edge()
        e48 = self.edges[48].display_edge()
        e49 = self.edges[49].display_edge()
        e50 = self.edges[50].display_edge()
        e51 = self.edges[51].display_edge()
        e52 = self.edges[52].display_edge()
        e53 = self.edges[53].display_edge()
        e54 = self.edges[54].display_edge()
        e55 = self.edges[55].display_edge()
        e56 = self.edges[56].display_edge()
        e57 = self.edges[57].display_edge()
        e58 = self.edges[58].display_edge()
        e59 = self.edges[59].display_edge()
        e60 = self.edges[60].display_edge()
        e61 = self.edges[61].display_edge()
        e62 = self.edges[62].display_edge()
        e63 = self.edges[63].display_edge()
        e64 = self.edges[64].display_edge()
        e65 = self.edges[65].display_edge()
        e66 = self.edges[66].display_edge()
        e67 = self.edges[67].display_edge()
        e68 = self.edges[68].display_edge()
        e69 = self.edges[69].display_edge()
        e70 = self.edges[70].display_edge()
        e71 = self.edges[71].display_edge()

        i00 = self.tiles[0].display_token()
        i01 = self.tiles[1].display_token()
        i02 = self.tiles[2].display_token()
        i03 = self.tiles[3].display_token()
        i04 = self.tiles[4].display_token()
        i05 = self.tiles[5].display_token()
        i06 = self.tiles[6].display_token()
        i07 = self.tiles[7].display_token()
        i08 = self.tiles[8].display_token()
        i09 = self.tiles[9].display_token()
        i10 = self.tiles[10].display_token()
        i11 = self.tiles[11].display_token()
        i12 = self.tiles[12].display_token()
        i13 = self.tiles[13].display_token()
        i14 = self.tiles[14].display_token()
        i15 = self.tiles[15].display_token()
        i16 = self.tiles[16].display_token()
        i17 = self.tiles[17].display_token()
        i18 = self.tiles[18].display_token()

        t00 = self.tiles[0].display_type()
        t01 = self.tiles[1].display_type()
        t02 = self.tiles[2].display_type()
        t03 = self.tiles[3].display_type()
        t04 = self.tiles[4].display_type()
        t05 = self.tiles[5].display_type()
        t06 = self.tiles[6].display_type()
        t07 = self.tiles[7].display_type()
        t08 = self.tiles[8].display_type()
        t09 = self.tiles[9].display_type()
        t10 = self.tiles[10].display_type()
        t11 = self.tiles[11].display_type()
        t12 = self.tiles[12].display_type()
        t13 = self.tiles[13].display_type()
        t14 = self.tiles[14].display_type()
        t15 = self.tiles[15].display_type()
        t16 = self.tiles[16].display_type()
        t17 = self.tiles[17].display_type()
        t18 = self.tiles[18].display_type()

        p00 = self.tiles[0].display_pips()
        p01 = self.tiles[1].display_pips()
        p02 = self.tiles[2].display_pips()
        p03 = self.tiles[3].display_pips()
        p04 = self.tiles[4].display_pips()
        p05 = self.tiles[5].display_pips()
        p06 = self.tiles[6].display_pips()
        p07 = self.tiles[7].display_pips()
        p08 = self.tiles[8].display_pips()
        p09 = self.tiles[9].display_pips()
        p10 = self.tiles[10].display_pips()
        p11 = self.tiles[11].display_pips()
        p12 = self.tiles[12].display_pips()
        p13 = self.tiles[13].display_pips()
        p14 = self.tiles[14].display_pips()
        p15 = self.tiles[15].display_pips()
        p16 = self.tiles[16].display_pips()
        p17 = self.tiles[17].display_pips()
        p18 = self.tiles[18].display_pips()

        h00 = self.harbors[0].display_harbor()
        h01 = self.harbors[1].display_harbor()
        h02 = self.harbors[2].display_harbor()
        h03 = self.harbors[3].display_harbor()
        h04 = self.harbors[4].display_harbor()
        h05 = self.harbors[5].display_harbor()
        h06 = self.harbors[6].display_harbor()
        h07 = self.harbors[7].display_harbor()
        h08 = self.harbors[8].display_harbor()

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
