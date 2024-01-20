import unittest

from src.catan.board.terrain import Desert, Fields, Forest, Hills, Mountains, Pasture
from src.catan.board.tile import Tile


class TestTile(unittest.TestCase):
    def setUp(self):
        self.field = Tile(type=Fields(), id=0)
        self.des = Tile(type=Desert(), id=1, robber=True)
        self.forest = Tile(type=Forest(), id=2)
        self.pasture = Tile(type=Pasture(), id=3)
        self.hills = Tile(type=Hills(), id=4)
        self.mountains = Tile(type=Mountains(), id=5)

    def test_repr(self):
        assert (
            repr(self.field)
            == "Tile(type=Fields, id=0, token=None, nodes=[0, 1, 2, 8, 9, 10], robber=False)"
        )

    def test_id(self):
        assert self.field.id == 0
        assert self.des.id == 1
        assert self.forest.id == 2
        assert self.pasture.id == 3
        assert self.hills.id == 4
        assert self.mountains.id == 5

    def test_token(self):
        assert self.field.token is None
        assert self.des.token is None
        assert self.forest.token is None
        assert self.pasture.token is None
        assert self.hills.token is None
        assert self.mountains.token is None

    def test_robber(self):
        assert self.field.robber is False
        assert self.des.robber is True
        assert self.forest.robber is False
        assert self.pasture.robber is False
        assert self.hills.robber is False
        assert self.mountains.robber is False

    def test_get_near_nodes(self):
        assert self.field.get_near_nodes() == [0, 1, 2, 8, 9, 10]
        assert self.des.get_near_nodes() == [2, 3, 4, 10, 11, 12]
        assert self.forest.get_near_nodes() == [4, 5, 6, 12, 13, 14]
        assert self.pasture.get_near_nodes() == [7, 8, 9, 17, 18, 19]
        assert self.hills.get_near_nodes() == [9, 10, 11, 19, 20, 21]
        assert self.mountains.get_near_nodes() == [11, 12, 13, 21, 22, 23]

    def test_tile(self):
        assert self.field.tile() == Fields()
        assert self.des.tile() == Desert()
        assert self.forest.tile() == Forest()
        assert self.pasture.tile() == Pasture()
        assert self.hills.tile() == Hills()
        assert self.mountains.tile() == Mountains()

    def test_value(self):
        assert self.field.value() is None
        assert self.des.value() is None
        assert self.forest.value() is None
        assert self.pasture.value() is None
        assert self.hills.value() is None
        assert self.mountains.value() is None

    def test_display_type(self):
        assert isinstance(self.field.display_type(), str)
        assert isinstance(self.des.display_type(), str)
        assert isinstance(self.forest.display_type(), str)
        assert isinstance(self.pasture.display_type(), str)
        assert isinstance(self.hills.display_type(), str)
        assert isinstance(self.mountains.display_type(), str)

    def test_display_id(self):
        assert isinstance(self.field.display_id(), str)
        assert isinstance(self.des.display_id(), str)
        assert isinstance(self.forest.display_id(), str)
        assert isinstance(self.pasture.display_id(), str)
        assert isinstance(self.hills.display_id(), str)
        assert isinstance(self.mountains.display_id(), str)

    def test_has_robber(self):
        assert self.field.has_robber() is False
        assert self.des.has_robber() is True
        assert self.forest.has_robber() is False
        assert self.pasture.has_robber() is False
        assert self.hills.has_robber() is False
        assert self.mountains.has_robber() is False

    def test_display_pips(self):
        self.des.robber = True

        self.field.token = 2
        self.des.token = 2
        self.forest.token = 2
        self.pasture.token = 2
        self.hills.token = 2
        self.mountains.token = 2

        assert isinstance(self.field.display_pips(), str)
        assert isinstance(self.des.display_pips(), str)
        assert isinstance(self.forest.display_pips(), str)
        assert isinstance(self.pasture.display_pips(), str)
        assert isinstance(self.hills.display_pips(), str)
        assert isinstance(self.mountains.display_pips(), str)

    def test_display_pips_desert_without_robber(self):
        self.des.robber = False

        self.des.token = 2

        assert isinstance(self.des.display_pips(), str)

    def test_display_pips_tile_with_robber(self):
        self.field.robber = True

        self.field.token = 2

        assert isinstance(self.field.display_pips(), str)

    def test_display_robber(self):
        self.des.robber = True

        assert self.des.display_robber() == "(R)"

    def test_display_robber_rmpty(self):
        self.des.robber = False

        assert self.des.display_robber() == "   "
