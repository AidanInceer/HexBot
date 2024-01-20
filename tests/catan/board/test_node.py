import unittest

from colorama import Fore

from src.catan.board.node import Node


class TestNode(unittest.TestCase):
    def setUp(self):
        self.node = Node(id=0)

    def test_id(self):
        assert self.node.id == 0

    def test_nodes(self):
        assert self.node.nodes == [1, 8]

    def test_edges(self):
        assert self.node.edges == [0, 6]

    def test_occupied(self):
        assert self.node.occupied is False

    def test_color(self):
        assert self.node.color is None

    def test_near_nodes(self):
        assert self.node.near_nodes() == [1, 8]

    def test_display_node_red(self):
        self.node.color = "Red"
        actual = self.node.display_node()
        assert isinstance(actual, str)

    def test_display_node_blue(self):
        self.node.color = "Blue"
        actual = self.node.display_node()
        assert isinstance(actual, str)

    def test_display_node_green(self):
        self.node.color = "Green"
        actual = self.node.display_node()
        assert isinstance(actual, str)

    def test_display_node_yellow(self):
        self.node.color = "Yellow"
        actual = self.node.display_node()
        assert isinstance(actual, str)

    def test_display_node_none(self):
        output = f"({str(self.node.id).zfill(2)})"
        assert self.node.display_node() == output

    def test_near_edges(self):
        assert self.node.near_edges() == [0, 6]

    def test_near_harbors(self):
        assert self.node.near_harbors() == [0]

    def test_near_tiles(self):
        assert self.node.near_tiles() == [0]
