from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Optional

from src.catan.board.edge import Edge
from src.catan.board.harbor import Harbor
from src.catan.board.node import Node
from src.catan.board.terrain import Desert, Fields, Forest, Hills, Mountains, Pasture
from src.catan.board.tile import Tile


@dataclass
class Board:
    """
    Represents a game board for the game of Catan.
    """

    nodes: Optional[List[Node]] = None
    edges: Optional[List[Edge]] = None
    harbors: Optional[List[Harbor]] = None
    tiles: Optional[List[Tile]] = None

    def _node(self, node_id: int) -> Node:
        """
        Returns the node with the given ID.

        Args:
            node_id (int): The ID of the node.

        Returns:
            Node: The node with the given ID.
        """
        return self.nodes[node_id]

    def _edge(self, edge_id: int) -> Edge:
        """
        Returns the edge with the given ID.

        Args:
            edge_id (int): The ID of the edge.

        Returns:
            Edge: The edge with the given ID.
        """
        return self.edges[edge_id]

    def _harbor(self, harbor_id: int) -> Harbor:
        """
        Returns the harbor with the given ID.

        Args:
            harbor_id (int): The ID of the harbor.

        Returns:
            Harbor: The harbor with the given ID.
        """
        return self.harbors[harbor_id]

    def active_tiles(self, roll: int) -> List[Tile]:
        """
        Returns a list of tiles that are active for the given roll.

        Args:
            roll (int): The roll value.

        Returns:
            List[Tile]: A list of active tiles for the given roll.
        """
        return [tile for tile in self.tiles if tile.token == roll]

    def set_robber_tile(self, selected_tile: Tile) -> Tile:
        """
        Sets the robber tile to the selected tile.

        Args:
            selected_tile (Tile): The selected tile.

        Returns:
            Tile: The selected tile.
        """
        for tile in self.tiles:
            if tile.id == selected_tile:
                return tile

    def get_robber_tile(self) -> Tile:
        """
        Returns the tile where the robber is currently located.

        Returns:
            Tile: The tile with the robber.
        """
        for tile in self.tiles:
            if tile.robber:
                return tile

    def generate(self) -> None:
        """
        Generates the nodes, edges, harbors, and tiles for the board.
        """
        self.nodes = self.generate_nodes()
        self.edges = self.generate_edges()
        self.harbors = self.generate_harbors()
        self.tiles = self.generate_tiles()

    def generate_nodes(self) -> List[Node]:
        """
        Generates the nodes for the board.

        Returns:
            List[Node]: A list of generated nodes.
        """
        self.nodes = [Node(id=node_id) for node_id in range(54)]
        return self.nodes

    def generate_edges(self) -> List[Edge]:
        """
        Generates the edges for the board.

        Returns:
            List[Edge]: A list of generated edges.
        """
        self.edges = [Edge(id=edge_id) for edge_id in range(72)]
        return self.edges

    def generate_harbors(self) -> List[Harbor]:
        """
        Generates the harbors for the board.

        Returns:
            List[Harbor]: A list of generated harbors.
        """
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
        """
        Generates the tiles for the board.

        Returns:
            List[Tile]: A list of generated tiles.
        """
        tile_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

        tile_types = (
            [Desert()]
            + [Fields()] * 4
            + [Forest()] * 4
            + [Pasture()] * 4
            + [Mountains()] * 3
            + [Hills()] * 3
        )
        # TODO: improve this shuffle
        random.shuffle(tile_types)

        self.tiles = [
            Tile(type=tile_type, id=tile_id)
            for tile_type, tile_id in zip(tile_types, tile_ids)
        ]

        for tile in self.tiles:
            if isinstance(tile.type, Desert):
                tile.robber = True

        self.apply_tokens()
        return self.tiles

    def apply_tokens(self) -> List[Tile]:
        """
        Applies tokens to the tiles.

        Returns:
            List[Tile]: A list of tiles with applied tokens.
        """
        tokens = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        for tile in self.tiles:
            if isinstance(tile.type, Desert):
                tile.token = None
            else:
                tile.token = random.choice(tokens)
                tokens.remove(tile.token)
        return self.tiles

    def display(self) -> None:
        """
        Displays the board.
        """
        n, e, i, t, p = [], [], [], [], []
        # create a lists of all nodes, edges, tiles and harbors.
        for j in range(54):
            n.append(self.nodes[j].display_node())

        for j in range(72):
            e.append(self.edges[j].display_edge())

        for j in range(19):
            i.append(self.tiles[j].display_token())
            t.append(self.tiles[j].display_type())
            p.append(self.tiles[j].display_pips())

        h = [self.harbors[i].display_harbor() for i in range(9)]

        board = f"""
===========================================================================================

                                                     {h[0]}
                                                         ||
                                                   {n[0]}--{e[0]}--{n[1]}
                                                  /              \\
                                                 {e[6]}               {e[1]}
                                                /        {i[0]}        \\
                                   {n[7]}--{e[10]}--{n[8]}     {t[0]}    {n[2]}--{e[2]}--{n[3]}
                                  /              \\      {p[0]}     /              \\
                  {h[3]}- - -{e[18]}               {e[11]}             {e[7]}               {e[3]}- - -{h[1]}
                                /        {i[3]}        \\            /        {i[1]}        \\
                   {n[16]}--{e[23]}--{n[17]}     {t[3]}    {n[9]}--{e[12]}--{n[10]}     {t[1]}    {n[4]}--{e[4]}--{n[5]}
                  /              \\      {p[3]}     /              \\      {p[1]}     /              \\
                 {e[33]}               {e[24]}             {e[19]}               {e[13]}             {e[8]}               {e[5]}
                /        {i[7]}        \\            /        {i[4]}        \\            /        {i[2]}        \\
             {n[27]}     {t[7]}    {n[18]}--{e[25]}--{n[19]}     {t[4]}    {n[11]}--{e[14]}--{n[12]}     {t[2]}    {n[6]}
                 \\      {p[7]}     /              \\      {p[4]}     /              \\      {p[2]}     /
                  {e[39]}             {e[34]}               {e[26]}             {e[20]}               {e[15]}             {e[9]}
                   \\            /        {i[8]}        \\            /        {i[5]}        \\            /
                   {n[28]}--{e[40]}--{n[29]}     {t[8]}    {n[20]}--{e[27]}--{n[21]}     {t[5]}    {n[13]}--{e[16]}--{n[14]}
                  /              \\      {p[8]}     /              \\      {p[5]}     /              \\
 {h[5]}- - -{e[49]}               {e[41]}             {e[35]}               {e[28]}             {e[21]}               {e[17]}- - -{h[2]}
                /        {i[12]}        \\            /        {i[9]}        \\            /        {i[6]}        \\
             {n[38]}     {t[12]}    {n[30]}--{e[42]}--{n[31]}     {t[9]}    {n[22]}--{e[29]}--{n[23]}     {t[6]}    {n[15]}
                 \\      {p[12]}     /              \\      {p[9]}     /              \\      {p[6]}     /
                  {e[54]}             {e[50]}               {e[43]}             {e[36]}               {e[30]}             {e[22]}
                   \\            /        {i[13]}        \\            /        {i[10]}        \\            /
                   {n[39]}--{e[55]}--{n[40]}     {t[13]}    {n[32]}--{e[44]}--{n[33]}     {t[10]}    {n[24]}--{e[31]}--{n[25]}
                  /              \\      {p[13]}     /              \\      {p[10]}     /              \\
                 {e[62]}               {e[56]}             {e[51]}               {e[45]}             {e[37]}               {e[32]}
                /        {i[16]}        \\            /        {i[14]}        \\            /        {i[11]}        \\
             {n[47]}     {t[16]}    {n[41]}--{e[57]}--{n[42]}     {t[14]}    {n[34]}--{e[46]}--{n[35]}     {t[11]}    {n[26]}
                 \\      {p[16]}     /              \\      {p[14]}     /              \\      {p[11]}     /
    {h[7]}- - -{e[66]}             {e[63]}               {e[58]}             {e[52]}               {e[47]}             {e[38]}- - -{h[4]}
                   \\            /        {i[17]}        \\            /        {i[15]}        \\            /
                   {n[48]}--{e[67]}--{n[49]}     {t[17]}    {n[43]}--{e[59]}--{n[44]}     {t[15]}    {n[36]}--{e[48]}--{n[37]}
                                 \\      {p[17]}     /              \\      {p[15]}     /
                                  {e[68]}             {e[64]}               {e[60]}             {e[53]}
                                   \\            /        {i[18]}        \\            /
                                   {n[50]}--{e[69]}--{n[51]}     {t[18]}    {n[45]}--{e[61]}--{n[46]}
                                                 \\      {p[18]}     /      ||
                                    {h[8]}- - -{e[70]}             {e[65]}   {h[6]}
                                                   \\            /
                                                   {n[52]}--{e[71]}--{n[53]}

==========================================================================================="""
        print(board)
