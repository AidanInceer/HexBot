import unittest
from unittest.mock import patch

from src.catan.board.board import Board
from src.catan.player.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(color="red", name="1", type="human")
        self.board = Board()
        self.board.generate()
        self.players = [
            Player(color="red"),
            Player(color="blue"),
            Player(color="green"),
            Player(color="yellow"),
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
