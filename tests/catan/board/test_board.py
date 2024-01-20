import unittest
from unittest.mock import patch

from src.catan.board.board import Board
from src.catan.board.tile import Tile


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.generate()

    def test_nodes(self):
        assert len(self.board.nodes) == 54

    def test_edges(self):
        assert len(self.board.edges) == 72

    def test_tiles(self):
        assert len(self.board.tiles) == 19

    @patch("src.catan.board.board.Board.generate_nodes")
    @patch("src.catan.board.board.Board.generate_edges")
    @patch("src.catan.board.board.Board.generate_harbors")
    @patch("src.catan.board.board.Board.generate_tiles")
    def test_generate(self, mock_tile, mock_harbor, mock_edge, mock_node):
        self.board.generate()
        mock_node.assert_called_once()
        mock_edge.assert_called_once()
        mock_harbor.assert_called_once()
        mock_tile.assert_called_once()

    def test_node(self):
        assert self.board._node(0).id == 0

    def test_edge(self):
        assert self.board._edge(0).id == 0

    def test_harbor(self):
        assert self.board._harbor(0).id == 0

    def test_tile(self):
        assert self.board._tile(0).id == 0

    def test_active_tiles_robber(self):
        tiles = self.board.active_tiles(7)
        assert len(tiles) == 0

    def test_active_tiles_two(self):
        tiles = self.board.active_tiles(2)
        assert len(tiles) == 1

    def test_active_tiles_three(self):
        tiles = self.board.active_tiles(3)
        assert len(tiles) == 2

    def test_active_tiles_four(self):
        tiles = self.board.active_tiles(4)
        assert len(tiles) == 2

    def test_set_robber_tile_instance(self):
        tile = self.board.set_robber_tile(0)
        assert isinstance(tile, Tile)

    def test_get_robber_tile(self):
        tile = self.board.set_robber_tile(0)
        assert self.board.get_robber_tile() == tile

    def test_generate_nodes(self):
        board = Board()
        board.generate_nodes()
        assert len(board.nodes) == 54

    def test_generate_edges(self):
        board = Board()
        board.generate_edges()
        assert len(board.edges) == 72

    def test_generate_harbors(self):
        board = Board()
        board.generate_harbors()
        assert len(board.harbors) == 9

    def test_generate_tiles(self):
        board = Board()
        board.generate_tiles()
        assert len(board.tiles) == 19

    def test_display(self):
        x = self.board.display()
        assert x is None
