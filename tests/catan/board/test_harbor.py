import unittest

from src.catan.board.harbor import Harbor


class TestHarbor(unittest.TestCase):
    def setUp(self):
        self.harbor = Harbor(0, "Brick", 3)

    def test_id(self):
        assert self.harbor.id == 0

    def test_resource(self):
        assert self.harbor.resource == "Brick"

    def test_rate(self):
        assert self.harbor.rate == 3

    def test_near_nodes(self):
        assert self.harbor.near_nodes() == [0, 1]

    def test_type(self):
        assert self.harbor.type() == "Brick"

    def test_trade_rate(self):
        assert self.harbor.trade_rate() == 3

    def test_display_harbor(self):
        assert self.harbor.display_harbor() == "[Brick 3:1]"
