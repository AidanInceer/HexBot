import unittest
from unittest.mock import Mock, patch

from src.catan.board.board import Board
from src.catan.buildings.buildings import City, Settlement
from src.catan.deck.deck import CardDeck
from src.catan.game.game import Game
from src.catan.player.player import Player
from src.config.config import load_config
from src.utils.handlers import PathHandler


class TestGame(unittest.TestCase):
    def setUp(self):
        config = load_config(PathHandler.config_path)

        deck = CardDeck()

        board = Board()
        board.generate()
        self.game = Game(
            players=[
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
            ],
            deck=deck,
            board=board,
            game_type="AUTO_SETUP",
            config=config,
        )

    def test_game_ended(self):
        assert self.game.game_ended is False

    @patch("src.catan.board.board.Board.display")
    @patch("src.catan.game.game.Game.auto_setup")
    @patch("src.catan.game.game.Game.game_setup")
    @patch("src.catan.game.game.Game.turn")
    def test_run(
        self,
        mock_turn: Mock,
        mock_game_setup: Mock,
        mock_auto_setup: Mock,
        mock_display: Mock,
    ):
        self.game.players[0].score = 10
        self.game.run()
        assert self.game.game_ended is True

    @patch("src.catan.player.player.Player.build")
    @patch("src.catan.board.board.Board.display")
    def test_auto_setup(self, mock_display: Mock, mock_build: Mock):
        self.game.auto_setup()
        mock_display.assert_called()
        mock_build.assert_called()

    @patch("src.catan.player.player.Player.build")
    def test_game_setup(self, mock_build: Mock):
        self.game.game_setup()
        mock_build.assert_called()

    def test_check_win_true(self):
        self.game.players[0].score = 10
        self.game.check_win()
        assert self.game.game_ended is True

    def test_check_win_false(self):
        self.game.check_win()
        assert self.game.game_ended is False

    @patch("src.catan.player.player.Player.build")
    @patch("src.catan.player.player.Player.trade")
    @patch("src.catan.player.player.Player.dev_card")
    @patch("src.catan.player.player.Player.roll")
    @patch("src.catan.game.game.Game.collect")
    @patch("builtins.input")
    def test_turn(
        self,
        self_mock_input: Mock,
        mock_collect: Mock,
        mock_roll: Mock,
        mock_dev_card: Mock,
        mock_trade: Mock,
        mock_build: Mock,
    ):
        self_mock_input.side_effect = ["1", "2", "3", "4"]
        self.game.turn(self.game.players[0])
        mock_collect.assert_called()
        mock_roll.assert_called()
        mock_build.assert_called()
        mock_dev_card.assert_called()
        mock_trade.assert_called()

    @patch("src.catan.game.game.Game.activate_robber")
    @patch("src.catan.player.player.Player.build")
    @patch("src.catan.player.player.Player.trade")
    @patch("src.catan.player.player.Player.dev_card")
    @patch("src.catan.player.player.Player.roll")
    @patch("src.catan.game.game.Game.collect")
    @patch("builtins.input")
    def test_turn_robber_called(
        self,
        self_mock_input: Mock,
        mock_collect: Mock,
        mock_roll: Mock,
        mock_dev_card: Mock,
        mock_trade: Mock,
        mock_build: Mock,
        mock_activate_robber: Mock,
    ):
        mock_roll.return_value = 7
        self_mock_input.side_effect = ["1", "2", "3", "4"]
        self.game.turn(self.game.players[0])
        mock_collect.assert_called()
        mock_roll.assert_called()
        mock_build.assert_called()
        mock_dev_card.assert_called()
        mock_trade.assert_called()
        mock_activate_robber.assert_called()

    @patch("src.catan.game.game.Game.collect_from_settlements")
    @patch("src.catan.game.game.Game.collect_from_cities")
    def test_collect(
        self, mock_collect_from_cities: Mock, mock_collect_from_settlements: Mock
    ):
        self.game.collect(6)
        mock_collect_from_cities.assert_called()
        mock_collect_from_settlements.assert_called()

    @patch("src.catan.game.game.Game.collect_from_settlements")
    @patch("src.catan.game.game.Game.collect_from_cities")
    def test_collect_robber(
        self, mock_collect_from_cities: Mock, mock_collect_from_settlements: Mock
    ):
        self.game.collect(7)
        mock_collect_from_cities.assert_not_called()
        mock_collect_from_settlements.assert_not_called()

    def test_collect_from_settlements_no_colletion(self):
        self.game.auto_setup()

        init = self.game.players[0].resources.total()

        self.game.collect_from_settlements(
            self.game.players[0], self.game.board.tiles[9]
        )
        assert self.game.players[0].resources.total() == init

    def test_collect_from_settlements(self):
        self.game.auto_setup()

        init = self.game.players[0].resources.total()

        self.game.collect_from_settlements(
            self.game.players[0], self.game.board.tiles[3]
        )
        assert self.game.players[0].resources.total() > init

    def test_collect_from_cities_no_colletion(self):
        self.game.auto_setup()

        init = self.game.players[0].resources.total()

        self.game.collect_from_cities(self.game.players[0], self.game.board.tiles[9])
        assert self.game.players[0].resources.total() == init

    def test_collect_from_cities(self):
        self.game.auto_setup()

        self.game.board.nodes[3].building = City(color="Red", id=0)

        self.game.players[0].buildings.cities.append(City(color="Red", id=0))

        init = self.game.players[0].resources.total()

        self.game.collect_from_cities(self.game.players[0], self.game.board.tiles[0])
        assert self.game.players[0].resources.total() > init

    @patch("src.catan.game.game.Game.move_robber_tile")
    @patch("src.catan.game.game.Game.determine_who_to_steal_from")
    @patch("src.catan.game.game.Game.select_player_to_steal_from")
    @patch("src.catan.game.game.Game.steal_random_resource")
    @patch("src.catan.game.game.Game.robber_discard_resources")
    def test_activate_robber(
        self,
        mock_robber_discard_resources: Mock,
        mock_steal_random_resource: Mock,
        mock_select_player_to_steal_from: Mock,
        mock_determine_who_to_steal_from: Mock,
        mock_move_robber_tile: Mock,
    ):
        self.game.activate_robber(self.game.players[0])
        mock_move_robber_tile.assert_called()
        mock_determine_who_to_steal_from.assert_called()
        mock_select_player_to_steal_from.assert_called()
        mock_steal_random_resource.assert_called()
        mock_robber_discard_resources.assert_called()

    @patch("src.catan.game.game.Game.move_robber_tile")
    @patch("src.catan.game.game.Game.determine_who_to_steal_from")
    @patch("src.catan.game.game.Game.select_player_to_steal_from")
    @patch("src.catan.game.game.Game.steal_random_resource")
    @patch("src.catan.game.game.Game.robber_discard_resources")
    def test_activate_robber_no_players(
        self,
        mock_robber_discard_resources: Mock,
        mock_steal_random_resource: Mock,
        mock_select_player_to_steal_from: Mock,
        mock_determine_who_to_steal_from: Mock,
        mock_move_robber_tile: Mock,
    ):
        mock_determine_who_to_steal_from.return_value = False
        self.game.activate_robber(self.game.players[0])
        mock_move_robber_tile.assert_called()
        mock_determine_who_to_steal_from.assert_called()
        mock_select_player_to_steal_from.assert_not_called()
        mock_steal_random_resource.assert_not_called()
        mock_robber_discard_resources.assert_called()

    @patch("src.catan.game.game.Game.move_robber_tile")
    @patch("src.catan.game.game.Game.determine_who_to_steal_from")
    @patch("src.catan.game.game.Game.select_player_to_steal_from")
    @patch("src.catan.game.game.Game.steal_random_resource")
    @patch("src.catan.game.game.Game.robber_discard_resources")
    def test_activate_robber_not_robbed(
        self,
        mock_robber_discard_resources: Mock,
        mock_steal_random_resource: Mock,
        mock_select_player_to_steal_from: Mock,
        mock_determine_who_to_steal_from: Mock,
        mock_move_robber_tile: Mock,
    ):
        mock_determine_who_to_steal_from.return_value = True
        mock_select_player_to_steal_from.return_value = False
        self.game.activate_robber(self.game.players[0])
        mock_move_robber_tile.assert_called()
        mock_determine_who_to_steal_from.assert_called()
        mock_select_player_to_steal_from.assert_called()
        mock_steal_random_resource.assert_not_called()
        mock_robber_discard_resources.assert_called()

    @patch("builtins.input", return_value="1")
    def test_move_robber_tile(self, mock_input):
        actual = self.game.move_robber_tile()
        assert actual.id == 1

    @patch("builtins.input", side_effect=["22", "2"])
    def test_move_robber_tile_invalid_tile(self, mock_input):
        actual = self.game.move_robber_tile()
        assert actual.id == 2

    @patch("builtins.input", side_effect=["3", "2"])
    def test_move_robber_tile_same_tile(self, mock_input):
        self.game.board.tiles[3].robber = True

        for tile in self.game.board.tiles:
            if tile.id != 3:
                tile.robber = False

        actual = self.game.move_robber_tile()
        assert actual.id == 2

    @patch("builtins.input", return_value="Red")
    def test_select_player_to_steal_from(self, mock_input):
        self.game.players[0].resources.wheat.count += 1
        actual = self.game.select_player_to_steal_from({"Red"})
        assert actual[0].color == "Red"

    @patch("builtins.input", return_value="Red")
    def test_select_player_to_steal_from_no_players(self, mock_input):
        for player in self.game.players:
            player.resources.wheat.count = 0
            player.resources.ore.count = 0
            player.resources.sheep.count = 0
            player.resources.brick.count = 0
            player.resources.wood.count = 0

        actual = self.game.select_player_to_steal_from(able_to_steal_from={})
        assert actual == []

    def test_steal_random_resource(self):
        for player in self.game.players:
            player.resources.wheat.count = 0
            player.resources.ore.count = 0
            player.resources.sheep.count = 0
            player.resources.brick.count = 0
            player.resources.wood.count = 0

        self.game.players[1].resources.ore.count = 1
        self.game.steal_random_resource([self.game.players[1]], self.game.players[0])
        assert self.game.players[0].resources.ore.count == 1

    def test_determine_who_to_steal_from_none(self):
        actual = self.game.determine_who_to_steal_from(
            self.game.players[0], self.game.board.tiles[0]
        )
        assert actual == set()

    def test_determine_who_to_steal_from_len_greater_than_one(self):
        self.game.auto_setup()

        actual = self.game.determine_who_to_steal_from(
            self.game.players[0], self.game.board.tiles[8]
        )
        assert actual == {"Blue", "Green"}

    def test_determine_who_to_steal_from_remove_self(self):
        self.game.auto_setup()

        actual = self.game.determine_who_to_steal_from(
            self.game.players[0], self.game.board.tiles[18]
        )
        assert actual == set()

    @patch("src.catan.player.player.Player.discard_resources")
    def test_robber_discard_resources(self, mock_discard: Mock):
        self.game.auto_setup()

        for player in self.game.players:
            player.resources.wheat.count = 0
            player.resources.ore.count = 0
            player.resources.sheep.count = 0
            player.resources.brick.count = 0
            player.resources.wood.count = 0

        self.game.players[0].resources.wheat.count = 8
        self.game.robber_discard_resources()
        mock_discard.assert_called_once()
