import collections
import unittest
from unittest.mock import patch

from src.catan.board.board import Board
from src.catan.buildings.buildings import Settlement
from src.catan.deck.cards import (
    Knight,
    Monopoly,
    RoadBuilding,
    VictoryPoint,
    YearOfPlenty,
)
from src.catan.deck.deck import CardDeck
from src.catan.player.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(color="red", name=0, type="human")
        self.board = Board()
        self.board.generate()
        self.players = [
            self.player,
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

    @patch("builtins.input", return_value=4)
    @patch("src.catan.player.player.Player.build")
    def test_build_settlement_no_resources(self, mock_build, mock_input):
        self.player.resources["wood"].count = 0
        self.player.resources["brick"].count = 0
        self.player.resources["sheep"].count = 0
        self.player.resources["wheat"].count = 0

        self.player.build_settlement(self.board, self.players)
        mock_build.return_value = None
        mock_build.assert_called_once()

    @patch("builtins.input", side_effect=[9, 1])
    def test_build_city(self, mock_input):
        self.player.build_settlement(self.board, self.players, auto=True)
        self.player.resources["ore"].count = 3
        self.player.resources["wheat"].count = 2
        self.player.resources["brick"].count = 0
        self.player.resources["wood"].count = 0
        self.player.resources["sheep"].count = 0
        self.player.build_city(self.board, self.players)

        assert self.board.nodes[9].occupied is True
        assert self.board.nodes[9].building.color == self.player.color
        assert self.board.nodes[9].building.id == 9
        assert self.board.nodes[9].color == self.player.color
        assert self.player.score == 2
        assert len(self.player.buildings.settlements) == 0
        assert len(self.player.buildings.cities) == 1
        assert self.board.nodes[8].occupied is True
        assert self.board.nodes[10].occupied is True
        assert self.board.nodes[19].occupied is True

    @patch("src.catan.player.player.Player.build", return_value=None)
    @patch("builtins.input", side_effect=[9, 1])
    def test_build_city_without_resources(self, mock_build, mock_input):
        self.player.resources["ore"].count = 0
        self.player.resources["wheat"].count = 0
        self.player.resources["brick"].count = 0
        self.player.resources["wood"].count = 0
        self.player.resources["sheep"].count = 0
        self.player.build_city(self.board, self.players)

        assert self.player.score == 0
        assert len(self.player.buildings.cities) == 0

    @patch("src.catan.player.player.Player.build", return_value=None)
    @patch("builtins.input", side_effect=[1, 9])
    def test_build_city_invlaid_location(self, mock_build, mock_input):  # NOSONAR
        self.player.build_settlement(self.board, self.players, auto=True)
        self.player.resources["ore"].count = 3
        self.player.resources["wheat"].count = 2
        self.player.resources["brick"].count = 0
        self.player.resources["wood"].count = 0
        self.player.resources["sheep"].count = 0
        self.player.build_city(self.board, self.players)

        assert self.board.nodes[9].occupied is True
        assert self.board.nodes[9].building.color == self.player.color
        assert self.board.nodes[9].building.id == 9
        assert self.board.nodes[9].color == self.player.color
        assert self.player.score == 2
        assert len(self.player.buildings.settlements) == 0
        assert len(self.player.buildings.cities) == 1
        assert self.board.nodes[8].occupied is True
        assert self.board.nodes[10].occupied is True
        assert self.board.nodes[19].occupied is True

    def test_replace_settlement(self):
        settle = Settlement(self.player.color, 1)
        self.player.buildings.settlements.append(settle)
        node = 1
        self.player.replace_settlement(node)
        assert self.player.buildings.settlements == []

    @patch("src.catan.player.player.Player.assign_longest_road", return_value=None)
    @patch("src.catan.player.player.Player.check_longest_road", return_value=None)
    @patch("src.catan.player.player.Player.build_road_default", return_value=None)
    def test_build_road(self, mock_default, mock_lr, mockalr):
        self.player.resources["wood"].count = 1
        self.player.resources["brick"].count = 1
        self.player.build_road(self.board, self.players, auto=False, dev_card=False)
        mock_default.assert_called_once()
        mock_lr.assert_called_once()
        mockalr.assert_called_once()

    @patch("src.catan.player.player.Player.assign_longest_road", return_value=None)
    @patch("src.catan.player.player.Player.check_longest_road", return_value=None)
    @patch("src.catan.player.player.Player.auto_build_road", return_value=None)
    def test_build_road_auto(self, mock_auto, mock_lr, mockalr):
        self.player.resources["wood"].count = 1
        self.player.resources["brick"].count = 1
        self.player.build_road(self.board, self.players, auto=True, dev_card=False)
        mock_auto.assert_called_once()
        mock_lr.assert_called_once()
        mockalr.assert_called_once()

    @patch("src.catan.player.player.Player.assign_longest_road", return_value=None)
    @patch("src.catan.player.player.Player.check_longest_road", return_value=None)
    @patch("src.catan.player.player.Player.build_road_dev_card", return_value=None)
    def test_build_road_dev(self, mock_dev, mock_lr, mockalr):
        self.player.resources["wood"].count = 0
        self.player.resources["brick"].count = 1
        self.player.build_road(self.board, self.players, auto=False, dev_card=True)
        mock_dev.assert_called_once()
        mock_lr.assert_called_once()
        mockalr.assert_called_once()

    @patch("src.catan.player.player.Player.assign_longest_road", return_value=None)
    @patch("src.catan.player.player.Player.check_longest_road", return_value=None)
    @patch("src.catan.player.player.Player.build", return_value=None)
    def test_build_road_not_enough_resources(self, mock_res, mock_lr, mockalr):
        self.player.resources["wood"].count = 0
        self.player.resources["brick"].count = 0
        self.player.build_road(self.board, self.players, auto=False, dev_card=False)
        mock_res.assert_called_once()
        mock_lr.assert_called_once()
        mockalr.assert_called_once()

    def test_dfs(self):
        graph = {1: [2, 3], 2: [4, 5], 3: [6], 4: [], 5: [], 6: []}
        visited = set()
        depth = self.player.dfs(graph, 1, visited)
        assert depth == 2

    def test_build_adjacency_list(self):
        # Create a sample board with some settlements and roads
        edges = [(1, 2), (2, 3), (2, 5), (2, 4), (1, 3), (3, 4), (4, 5), (5, 6)]

        # Call the build_adjacency_list method
        adjacency_list = self.player.build_adjacency_list(edges)

        # Check if the adjacency list is built correctly
        assert adjacency_list == collections.OrderedDict(
            [(1, [2, 3]), (2, [3, 4, 5]), (3, [4]), (4, [5]), (5, [6])]
        )

    def test_assign_longest_road(self):
        player_road_lengths = {}
        for player in self.players:
            player_road_lengths[player] = 0

        self.player.assign_longest_road(
            player_road_lengths,
            self.players,
        )
        assert self.players[0].longest_road is False
        assert self.players[1].longest_road is False
        assert self.players[2].longest_road is False
        assert self.players[3].longest_road is False

    def test_assign_longest_road_steal_lr(self):
        player_road_lengths = {
            self.players[0]: 5,
            self.players[1]: 1,
            self.players[2]: 1,
            self.players[3]: 1,
        }

        self.player.assign_longest_road(
            player_road_lengths,
            self.players,
        )
        assert self.players[0].longest_road is True
        assert self.players[1].longest_road is False
        assert self.players[2].longest_road is False
        assert self.players[3].longest_road is False

    def test_assign_longest_road_len_five(self):
        self.players[1].longest_road = True
        player_road_lengths = {
            self.players[0]: 6,
            self.players[1]: 5,
            self.players[2]: 1,
            self.players[3]: 1,
        }

        self.player.assign_longest_road(
            player_road_lengths,
            self.players,
        )
        assert self.players[0].longest_road is True
        assert self.players[1].longest_road is False
        assert self.players[2].longest_road is False
        assert self.players[3].longest_road is False

    @patch("builtins.input", side_effect=[0, 0, 1, 2, 3, 4])
    def test_check_longest_road(self, mock_build_road):
        self.player.build_settlement(self.board, self.players, auto=False)
        self.player.resources["wood"].count = 5
        self.player.resources["brick"].count = 5
        self.player.build_road_default(self.board, self.players)
        self.player.build_road_default(self.board, self.players)
        self.player.build_road_default(self.board, self.players)
        self.player.build_road_default(self.board, self.players)
        self.player.build_road_default(self.board, self.players)

        longest_road = self.player.check_longest_road(self.board, self.players)

        self.assertEqual(longest_road[self.player], 5)

    @patch("src.catan.player.player.Player.build_road", return_value=None)
    @patch("builtins.input", return_value=1)
    def test_build_road_default_invalid(self, mock_input, mock_build_road):
        self.player.resources["wood"].count = 1
        self.player.resources["brick"].count = 1
        self.player.build_road_default(self.board, self.players)
        self.assertEqual(self.player.resources["wood"].count, 1)
        self.assertEqual(self.player.resources["brick"].count, 1)
        mock_build_road.assert_called_once()

    @patch("builtins.input", side_effect=[1, 1])
    def test_build_road_dev_card(self, mock_input):
        self.player.build_settlement(self.board, self.players, auto=False)
        self.player.resources["wood"].count = 1
        self.player.resources["brick"].count = 1
        self.player.build_road_dev_card(self.board, self.players)
        self.assertEqual(self.player.resources["wood"].count, 1)
        self.assertEqual(self.player.resources["brick"].count, 1)

    @patch("src.catan.player.player.Player.build_road", return_value=None)
    @patch("builtins.input", side_effect=[0, 10])
    def test_build_road_dev_card_invalid_location(self, mock_input, mock_build_road):
        self.player.build_settlement(self.board, self.players, auto=False)
        self.player.resources["wood"].count = 1
        self.player.resources["brick"].count = 1
        self.player.build_road_dev_card(self.board, self.players)
        self.assertEqual(self.player.resources["wood"].count, 1)
        self.assertEqual(self.player.resources["brick"].count, 1)

        mock_build_road.assert_called_once()

    @patch("src.catan.player.player.Player.player_trade")
    @patch("builtins.input", return_value=1)
    def test_trade_only_player_trade(self, mock_input, mock_player_trade):
        self.player.trade(self.board, self.players)

        mock_player_trade.assert_called_once()

    @patch("src.catan.player.player.Player.bank_port_trade")
    @patch("builtins.input", return_value=2)
    def test_trade_only_bank_port_trade(self, mock_input, mock_bank_port_trade):
        self.player.trade(self.board, self.players)

        mock_bank_port_trade.assert_called_once()

    @patch("src.catan.player.player.Player.player_trade")
    @patch("builtins.input", return_value=3)
    def test_trade_cancel(self, mock_input, mock_player_trade):
        actual = self.player.trade(self.board, self.players)

        self.assertIsNone(actual)

    @patch("builtins.input", side_effect=["brick", "wood"])
    def test_bank_port_trade(self, mock_input):
        self.player.resources["brick"].count = 4
        self.player.resources["wood"].count = 4
        rates = {
            "brick": 4,
            "wood": 4,
            "sheep": 4,
            "wheat": 4,
            "ore": 4,
        }
        self.player.bank_port_trade(rates, self.board, self.players)

        self.assertEqual(self.player.resources["brick"].count, 0)
        self.assertEqual(self.player.resources["wood"].count, 5)

    @patch("src.catan.player.player.Player.trade")
    @patch("builtins.input", side_effect=["brick", "wood"])
    def test_bank_port_trade_not_enough(self, mock_input, mock_trade):
        self.player.resources["brick"].count = 0
        self.player.resources["wood"].count = 4
        rates = {
            "brick": 4,
            "wood": 4,
            "sheep": 4,
            "wheat": 4,
            "ore": 4,
        }
        self.player.bank_port_trade(rates, self.board, self.players)

        self.assertEqual(self.player.resources["brick"].count, 0)
        self.assertEqual(self.player.resources["wood"].count, 4)

    @patch("builtins.input", side_effect=["brick", 4, "wood", 4, "N", "Y", "N"])
    def test_player_trade(self, mock_input):
        self.player.resources["brick"].count = 4
        self.player.resources["wood"].count = 4
        self.players[2].resources["brick"].count = 4
        self.players[2].resources["wood"].count = 4
        self.player.player_trade(self.players)

        self.assertEqual(self.player.resources["brick"].count, 8)
        self.assertEqual(self.player.resources["wood"].count, 0)
        self.assertEqual(self.players[2].resources["brick"].count, 0)
        self.assertEqual(self.players[2].resources["wood"].count, 8)

    def test_determine_trade_rates(self):
        s4 = Settlement(self.player.color, 4)
        self.player.buildings.settlements.append(s4)
        self.board.harbors[4].rate = 2
        self.board.harbors[4].resource = "wheat"
        rates = self.player.determine_trade_rates(self.board)

        self.assertEqual(
            rates, {"brick": 4, "wood": 4, "sheep": 4, "wheat": 2, "ore": 4}
        )

    def test_determine_trade_rates_all(self):
        s4 = Settlement(self.player.color, 4)
        self.player.buildings.settlements.append(s4)
        self.board.harbors[1].rate = 3
        self.board.harbors[1].resource = "all"
        rates = self.player.determine_trade_rates(self.board)

        self.assertEqual(
            rates, {"brick": 3, "wood": 3, "sheep": 3, "wheat": 3, "ore": 3, "all": 3}
        )

    @patch("src.catan.player.player.Player.collect_dev_card")
    @patch("src.catan.player.player.Player.select_dev_card_to_play")
    @patch("builtins.input", side_effect=[1, 2, 3])
    def test_dev_card(self, mock_input, mock_select, mock_collect):
        deck = CardDeck()
        self.player.dev_card(self.board, self.players, deck)
        mock_select.assert_called_once()
        mock_collect.assert_called_once()

    def test_collect_dev_card(self):
        deck = CardDeck()
        self.player.resources["sheep"].count = 1
        self.player.resources["wheat"].count = 1
        self.player.resources["ore"].count = 1
        self.player.collect_dev_card(deck)
        self.assertEqual(len(self.player.cards), 1)

    @patch("src.catan.player.player.Player.play_dev_card")
    @patch("builtins.input", side_effect=["knight"])
    def test_select_dev_card_to_play(self, mock_input, mock_play):
        self.player.cards = [Knight(color="red", played=False, player="red")]
        self.player.select_dev_card_to_play(self.board, self.players)
        mock_play.assert_called_once()

    @patch("src.catan.player.player.Player.play_knight")
    def test_play_dev_card_knight(self, mock_play):
        card = Knight(color="red", played=False, player="red")
        self.player.cards = [card]

        self.player.play_dev_card(card, self.board, self.players)
        self.assertEqual(len(self.player.cards), 0)
        mock_play.assert_called_once()

    @patch("src.catan.player.player.Player.play_victory_point")
    def test_play_dev_card_play_victory_point(self, mock_play):
        card = VictoryPoint(color="red", played=False, player="red")
        self.player.cards = [card]

        self.player.play_dev_card(card, self.board, self.players)
        self.assertEqual(len(self.player.cards), 0)
        mock_play.assert_called_once()

    @patch("src.catan.player.player.Player.play_monopoly")
    def test_play_dev_card_play_monopoly(self, mock_play):
        card = Monopoly(color="red", played=False, player="red")
        self.player.cards = [card]

        self.player.play_dev_card(card, self.board, self.players)
        self.assertEqual(len(self.player.cards), 0)
        mock_play.assert_called_once()

    @patch("src.catan.player.player.Player.play_road_building")
    def test_play_dev_card_play_road_building(self, mock_play):
        card = RoadBuilding(color="red", played=False, player="red")
        self.player.cards = [card]

        self.player.play_dev_card(card, self.board, self.players)
        self.assertEqual(len(self.player.cards), 0)
        mock_play.assert_called_once()

    @patch("src.catan.player.player.Player.play_year_of_plenty")
    def test_play_dev_card_play_year_of_plenty(self, mock_play):
        card = YearOfPlenty(color="red", played=False, player="red")
        self.player.cards = [card]

        self.player.play_dev_card(card, self.board, self.players)
        self.assertEqual(len(self.player.cards), 0)
        mock_play.assert_called_once()

    @patch("src.catan.player.player.Player.activate_knight")
    @patch("src.catan.player.player.Player.check_largest_army")
    def test_play_knight(self, mock_check, mock_activate):
        self.player.play_knight(self.board, self.players)
        mock_check.assert_called_once()
        mock_activate.assert_called_once()

    def test_victory_point(self):
        self.player.play_victory_point()
        self.assertEqual(self.player.score, 1)

    @patch("builtins.input", side_effect=["brick"])
    def test_play_monopoly(self, mock_input):
        self.player.resources["brick"].count = 0
        self.player.resources["wood"].count = 0
        self.player.resources["sheep"].count = 0
        self.player.resources["wheat"].count = 0
        self.player.resources["ore"].count = 0

        self.players[1].resources["brick"].count = 1
        self.players[2].resources["brick"].count = 1
        self.players[3].resources["brick"].count = 1

        self.player.play_monopoly(self.players)
        self.assertEqual(self.player.resources["brick"].count, 3)

    @patch("src.catan.player.player.Player.build_road")
    def test_play_road_building(self, mock_build):
        self.player.play_road_building(self.board, self.players)
        mock_build.assert_called()

    @patch("builtins.input", side_effect=["brick", "wood"])
    def test_play_year_of_plenty(self, mock_input):
        self.player.resources["brick"].count = 0
        self.player.resources["wood"].count = 0
        self.player.play_year_of_plenty()
        self.assertEqual(self.player.resources["brick"].count, 1)
        self.assertEqual(self.player.resources["wood"].count, 1)

    def test_total_resources(self):
        self.player.resources["brick"].count = 1
        self.player.resources["wood"].count = 1
        self.player.resources["sheep"].count = 1
        self.player.resources["wheat"].count = 1
        self.player.resources["ore"].count = 1

        self.assertEqual(self.player.total_resources(), 5)

    @patch("builtins.input", side_effect=["brick", "other", "brick", "brick", "brick"])
    def test_discard_resources(self, mock_input):
        self.player.resources["brick"].count = 8
        self.player.resources["wood"].count = 0
        self.player.resources["sheep"].count = 0
        self.player.resources["wheat"].count = 0
        self.player.resources["ore"].count = 0

        self.player.discard_resources(8)
        self.assertEqual(self.player.total_resources(), 4)
