import unittest

from colorama import Fore

from src.catan.board.edge import Edge


class TestEdge(unittest.TestCase):
    def setUp(self):
        self.edge = Edge(id=0)

    def test_id(self):
        assert self.edge.id == 0

    def test_nodes(self):
        assert self.edge.nodes == [0, 1]

    def test_edges(self):
        assert self.edge.edges == [1, 6]

    def test_occupied(self):
        assert self.edge.occupied is False

    def test_color(self):
        assert self.edge.color is None

    def test_near_nodes(self):
        assert self.edge.near_nodes() == [0, 1]

    def test_display_edge_red(self):
        self.edge.color = "Red"
        output = f"{Fore.RED + str(self.edge.id).zfill(2) + Fore.RESET}"
        assert self.edge.display_edge() == output

    def test_display_edge_blue(self):
        self.edge.color = "Blue"
        output = f"{Fore.BLUE + str(self.edge.id).zfill(2) + Fore.RESET}"
        assert self.edge.display_edge() == output

    def test_display_edge_green(self):
        self.edge.color = "Green"
        output = f"{Fore.GREEN + str(self.edge.id).zfill(2) + Fore.RESET}"
        assert self.edge.display_edge() == output

    def test_display_edge_yellow(self):
        self.edge.color = "Yellow"
        output = f"{Fore.YELLOW + str(self.edge.id).zfill(2) + Fore.RESET}"
        assert self.edge.display_edge() == output

    def test_display_edge_none(self):
        output = f"{str(self.edge.id).zfill(2)}"
        assert self.edge.display_edge() == output

    def test_hash(self):
        edge1 = Edge(id=0)
        edge2 = Edge(id=0)
        assert hash(edge1) == hash(edge2)
