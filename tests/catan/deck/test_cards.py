import unittest

from src.catan.deck.cards import (
    Knight,
    Monopoly,
    RoadBuilding,
    VictoryPoint,
    YearOfPlenty,
)


class TestKnight(unittest.TestCase):
    def setUp(self):
        self.knight = Knight()
        self.knight.color = "red"
        self.knight.played = True
        self.knight.player = "John"

    def test_color(self):
        assert self.knight.color == "red"

    def test_played(self):
        assert self.knight.played is True

    def test_player(self):
        assert self.knight.player == "John"

    def test_get_item(self):
        assert self.knight["color"] == "red"
        assert self.knight["played"] is True
        assert self.knight["player"] == "John"


class TestMonopoly(unittest.TestCase):
    def setUp(self):
        self.monopoly = Monopoly()
        self.monopoly.color = "red"
        self.monopoly.played = True
        self.monopoly.player = "John"

    def test_color(self):
        assert self.monopoly.color == "red"

    def test_played(self):
        assert self.monopoly.played is True

    def test_player(self):
        assert self.monopoly.player == "John"

    def test_get_item(self):
        assert self.monopoly["color"] == "red"
        assert self.monopoly["played"] is True
        assert self.monopoly["player"] == "John"


class TestRoadBuilding(unittest.TestCase):
    def setUp(self):
        self.road_building = RoadBuilding()
        self.road_building.color = "red"
        self.road_building.played = True
        self.road_building.player = "John"

    def test_color(self):
        assert self.road_building.color == "red"

    def test_played(self):
        assert self.road_building.played is True

    def test_player(self):
        assert self.road_building.player == "John"

    def test_get_item(self):
        assert self.road_building["color"] == "red"
        assert self.road_building["played"] is True
        assert self.road_building["player"] == "John"


class TestVictoryPoint(unittest.TestCase):
    def setUp(self):
        self.victory_point = VictoryPoint()
        self.victory_point.color = "red"
        self.victory_point.played = True
        self.victory_point.player = "John"

    def test_color(self):
        assert self.victory_point.color == "red"

    def test_played(self):
        assert self.victory_point.played is True

    def test_player(self):
        assert self.victory_point.player == "John"

    def test_get_item(self):
        assert self.victory_point["color"] == "red"
        assert self.victory_point["played"] is True
        assert self.victory_point["player"] == "John"


class TestYearOfPlenty(unittest.TestCase):
    def setUp(self):
        self.year_of_plenty = YearOfPlenty()
        self.year_of_plenty.color = "red"
        self.year_of_plenty.played = True
        self.year_of_plenty.player = "John"

    def test_color(self):
        assert self.year_of_plenty.color == "red"

    def test_played(self):
        assert self.year_of_plenty.played is True

    def test_player(self):
        assert self.year_of_plenty.player == "John"

    def test_get_item(self):
        assert self.year_of_plenty["color"] == "red"
        assert self.year_of_plenty["played"] is True
        assert self.year_of_plenty["player"] == "John"
