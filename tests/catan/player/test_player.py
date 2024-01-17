import unittest
from unittest.mock import patch

from src.catan.board.board import Board
from src.catan.buildings.buildings import Settlement
from src.catan.player.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(color="red", name=0, type="human")
        self.board = Board()
        self.board.generate()
        self.players = [
            Player(
                name=0,
                color="Red",
            ),
            Player(
                name=1,
                color="Yellow",
            ),
            Player(
                name=2,
                color="Blue",
            ),
            Player(
                name=3,
                color="Green",
            ),
        ]

    def test_roll_high(self):
        with patch("random.randint", return_value=7):
            roll = self.player.roll()
            self.assertEqual(roll, 14)

    def test_roll_low(self):
        with patch("random.randint", return_value=1):
            roll = self.player.roll()
            self.assertEqual(roll, 2)

    def test_roll_type(self):
        roll = self.player.roll()
        self.assertIsInstance(roll, int)

    @patch("src.catan.player.player.Player.build_settlement", return_value=None)
    @patch("src.catan.player.player.Player.build_road", return_value=None)
    @patch("src.catan.player.player.Player.build_city", return_value=None)
    @patch("src.catan.board.board.Board.display", return_value=None)
    def test_build_auto_setup(
        self, mock_display, mock_build_city, mock_build_road, mock_build_settlement
    ):
        self.player.build(self.board, self.players, setup=True, auto=True)

        self.assertEqual(mock_build_road.call_count, 1)
        self.assertEqual(mock_build_settlement.call_count, 1)
        assert self.player.end_building is True

    @patch("src.catan.player.player.Player.build_settlement", return_value=None)
    @patch("src.catan.player.player.Player.build_road", return_value=None)
    @patch("src.catan.player.player.Player.build_city", return_value=None)
    @patch("src.catan.board.board.Board.display", return_value=None)
    def test_build_setup(
        self, mock_display, mock_build_city, mock_build_road, mock_build_settlement
    ):
        self.player.build(self.board, self.players, setup=True, auto=False)

        self.assertEqual(mock_build_road.call_count, 1)
        self.assertEqual(mock_build_settlement.call_count, 1)
        self.assertEqual(mock_display.call_count, 2)
        assert self.player.end_building is True

    @patch("src.catan.player.player.Player.build_settlement", return_value=None)
    @patch("src.catan.player.player.Player.build_road", return_value=None)
    @patch("src.catan.player.player.Player.build_city", return_value=None)
    @patch("src.catan.board.board.Board.display", return_value=None)
    @patch("builtins.input", side_effect=[1, 2, 3, 4])
    def test_build(
        self,
        mock_input,
        mock_display,
        mock_build_city,
        mock_build_road,
        mock_build_settlement,
    ):
        self.player.build(self.board, self.players, setup=False, auto=False)

        self.assertEqual(mock_build_road.call_count, 1)
        self.assertEqual(mock_build_city.call_count, 1)
        self.assertEqual(mock_build_settlement.call_count, 1)
        assert self.player.end_building is True

    @patch("builtins.input", return_value=1)
    def test_build_settlement(self, mock_input):
        self.player.build_settlement(self.board, self.players, auto=False)

        settlement = Settlement(self.player.color, 1)

        assert self.board.nodes[1].occupied is True
        assert self.board.nodes[1].building == settlement
        assert self.board.nodes[1].color == self.player.color
        assert self.player.resources["wood"].count == 3
        assert self.player.resources["brick"].count == 3
        assert self.player.resources["sheep"].count == 1
        assert self.player.resources["wheat"].count == 1
        assert self.player.score == 1
        assert len(self.player.buildings.settlements) == 1
        assert self.board.nodes[0].occupied is True
        assert self.board.nodes[2].occupied is True

    @patch("builtins.input", side_effect=[1, 10])
    def test_build_settlement_invalid_location(self, mock_input):
        self.board.nodes[1].occupied = True
        self.player.build_settlement(self.board, self.players, auto=False)
        settlement = Settlement(self.player.color, 10)

        assert self.board.nodes[10].occupied is True
        assert self.board.nodes[10].building == settlement
        assert self.board.nodes[10].color == self.player.color
        assert self.player.resources["wood"].count == 3
        assert self.player.resources["brick"].count == 3
        assert self.player.resources["sheep"].count == 1
        assert self.player.resources["wheat"].count == 1
        assert self.player.score == 1
        assert len(self.player.buildings.settlements) == 1
        assert self.board.nodes[2].occupied is True
        assert self.board.nodes[9].occupied is True
        assert self.board.nodes[11].occupied is True

    @patch("builtins.input", side_effect=[1])
    def test_build_settlement_auto(self, mock_input):
        self.player.build_settlement(self.board, self.players, auto=True)
        settlement = Settlement(self.player.color, 9)

        assert self.board.nodes[9].occupied is True
        assert self.board.nodes[9].building == settlement
        assert self.board.nodes[9].color == self.player.color
        assert self.player.resources["wood"].count == 3
        assert self.player.resources["brick"].count == 3
        assert self.player.resources["sheep"].count == 1
        assert self.player.resources["wheat"].count == 1
        assert self.player.score == 1
        assert len(self.player.buildings.settlements) == 1
        assert self.board.nodes[8].occupied is True
        assert self.board.nodes[10].occupied is True
        assert self.board.nodes[19].occupied is True

    @patch("builtins.input", side_effect=[1])
    def test_build_settlement_auto_second(self, mock_input):
        self.board.nodes[9].occupied = True
        self.player.build_settlement(self.board, self.players, auto=True)

        assert self.board.nodes[43].occupied is True
