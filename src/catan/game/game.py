import random
from dataclasses import dataclass, field
from typing import List

from colorama import Fore

from src.catan.board.board import Board
from src.catan.board.tile import Tile
from src.catan.buildings.buildings import City, Settlement
from src.catan.deck.deck import CardDeck
from src.catan.player.player import Player
from src.catan.resources.resources import Brick, Ore, Sheep, Wheat, Wood
from src.catan.game.robber.robber_manager import RobberManager
from src.config.config import CentralConfig
from src.interface.input_handler import InputHandler
from src.interface.display_handler import TerminalDisplayHandler
from src.interface.protocols import DisplayHandlerProtocol, InputHandlerProtocol

TYPES = (
    Brick,
    Ore,
    Sheep,
    Wheat,
    Wood,
)


@dataclass
class Game:
    players: list[Player]
    deck: CardDeck
    game_type: str
    config: CentralConfig
    board: Board = field(default_factory=Board)
    game_ended: bool = False
    display_handler: DisplayHandlerProtocol = field(default_factory=TerminalDisplayHandler)
    input_handler: InputHandlerProtocol = field(
        default_factory=lambda: InputHandler(range(0), "human", "int")
    )  # Default for compat, will be overridden or used as factory base.
    # Actually, better to just default to None or a concrete default if dataclass field issues arise,
    # but since InputHandler is stateful per query, we might need a factory or just pass the wrapper.
    # Let's use field(init=False) or just inject it in __post_init__ or run if needed.
    # For now, let's just add it as an optional field or with default.

    def __post_init__(self):
        self.robber_manager = RobberManager(self.board, self.players)

    def run(self) -> None:
        self.display_handler.update_board(self.board)
        if self.game_type in self.config.options.auto_types:
            self.auto_setup()
        else:
            self.game_setup()
        while not self.game_ended:
            for player in self.players:
                self.turn(player)
                self.check_win()

    def auto_setup(self) -> None:
        """
        Automatically sets up the game by allowing each player to build their initial settlements and roads.
        """
        for player in self.players:
            player.build(self.board, self.players, setup=True, auto=True)

        for player in self.players[::-1]:
            player.build(self.board, self.players, setup=True, auto=True)
        self.display_handler.update_board(self.board)

    def game_setup(self) -> None:
        """
        Performs the game setup phase where each player takes turns to set up their initial settlements and roads.
        """

        for player in self.players:
            self.display_handler.message(f"{player.color}'s turn to setup")
            player.build(self.board, self.players, setup=True, auto=False)

        for player in self.players[::-1]:
            self.display_handler.message(f"{player.color}'s turn to setup")
            player.build(self.board, self.players, setup=True, auto=False)

    def check_win(self) -> None:
        """
        Checks if any player has reached a score of 10 or more and ends the game if so.
        """
        for player in self.players:
            if player.score >= 10:
                self.game_ended = True
                self.display_handler.message(f"{player.color} won!")

                for player in self.players:
                    self.display_handler.message(f"{player.color} had {player.score} points at the end of the game")
                break

    def turn(self, player: Player) -> None:
        """
        Executes a turn for the specified player in the game.

        Args:
            player (Player): The player whose turn it is.

        Returns:
            None
        """

        self.turn_ended = False
        self.display_handler.update_board(self.board)

        roll = player.roll()
        if roll == 7:
            self.activate_robber(player)

        self.collect(roll)

        self.display_user_info(player)

        while not self.turn_ended:
            turn_options = self.limit_turn_options(player)

            # Re-using input_handler instance or creating new specific query?
            # The original code created new InputHandler every time.
            # We can use the injected one if it supports 'process' with args, but the original class took args in __init__.
            # We updated InputHandler to take args in __init__ but delegate to backend.
            # Ideally we want `self.input_handler.process(options, type, msg)`
            # So let's instantiate the wrapping InputHandler using our factory or just use the protocol directly if we refactored enough.
            # The previous step kept InputHandler taking init args.
            choice = InputHandler(
                value_range=turn_options,
                user=player.type,
                input_type="int",
                message="1=Build, 2=Trade, 3=Dev Cards(Play/Select), 4=End: ",
                handler_backend=self.input_handler if hasattr(self.input_handler, "process") else None,
                # If self.input_handler IS the backend (TerminalInputHandler), we pass it.
            ).process()
            if choice == 1:
                player.build(self.board, self.players, setup=False, auto=False)
            elif choice == 2:
                player.trade(self.board, self.players)
            elif choice == 3:
                player.dev_card(self.board, self.players, self.deck)
            elif choice == 4:
                self.turn_ended = True

    def display_user_info(self, player: Player):
        if player.color == "Red":
            print_col = Fore.RED
        elif player.color == "Blue":
            print_col = Fore.BLUE
        elif player.color == "Green":
            print_col = Fore.GREEN
        elif player.color == "Yellow":
            print_col = Fore.YELLOW

        active_cards = [card.name for card in player.cards if card.played]

        self.display_handler.message(
            f"{print_col}"
            + f"{player.color}'s turn   Score: {player.score} Longest Road:{player.longest_road} Largest Army:{player.largest_army}  Cards: {active_cards}   {player.resources}"
            + f"{Fore.RESET}"
        )
        self.display_handler.message(
            "  \n==========================================================================================="
        )

    def collect(self, roll: int) -> None:
        """
        Collect resources from settlements and cities on active tiles for each player.

        Args:
            roll (int): The roll of the dice.

        Returns:
            None
        """
        for player in self.players:
            active_tiles = [tile for tile in self.board.active_tiles(roll) if not tile.robber]

            for tile in active_tiles:
                self.collect_from_settlements(player, tile)
                self.collect_from_cities(player, tile)

    def collect_from_settlements(self, player: Player, tile: Tile) -> None:
        """
        Collect resources from settlements on a given tile.

        Args:
            player (Player): The player collecting resources.
            tile (Tile): The tile from which resources are collected.

        Returns:
            None
        """
        active_nodes = [settlement.id for settlement in player.buildings.settlements]
        tile_nodes = tile.nodes

        if any(node in active_nodes for node in tile_nodes):
            player.resources[tile.type.produces].count += 1
            self.display_handler.message(f"{player.color} collected {tile.type.produces}.")

    def collect_from_cities(self, player: Player, tile: Tile) -> None:
        """
        Collect resources from cities built by the player on a given tile.

        Args:
            player (Player): The player who owns the cities.
            tile (Tile): The tile from which resources are collected.

        Returns:
            None
        """
        active_nodes = [city.id for city in player.buildings.cities]
        tile_nodes = tile.nodes

        if any(node in active_nodes for node in tile_nodes):
            player.resources[tile.type.produces].count += 2
            self.display_handler.message(f"{player.color} collected {tile.type.produces}.")

    def activate_robber(self, current_player: Player) -> None:
        new_robber_tile = self.move_robber_tile(current_player)

        # choose a player to steal a random resource from
        # if the player has no resources, they are skipped
        able_to_steal_from = self.determine_who_to_steal_from(current_player, new_robber_tile)

        if able_to_steal_from:
            robbed_player = self.select_player_to_steal_from(current_player, able_to_steal_from)
            if robbed_player:
                self.steal_random_resource(robbed_player, current_player)

        # if any player has more than 7 cards, they must discard half
        self.robber_discard_resources()

    def move_robber_tile(self, player) -> Tile:
        robber_tile = self.board.get_robber_tile()
        robber_moved = False

        while not robber_moved:
            move_robber = InputHandler(
                value_range=range(0, 18, 1),
                user=player.type,
                input_type="int",
                message="Choosen a Tile [0-18] to move the Robber to: ",
                handler_backend=self.input_handler if hasattr(self.input_handler, "process") else None,
            ).process()
            if move_robber < 0 or move_robber > 18:
                self.display_handler.message("Invalid tile.")
            elif move_robber == robber_tile.id:
                self.display_handler.message("Robber must be moved to a different tile.")
            else:
                new_robber_tile = self.board.set_robber_tile(move_robber)
                new_robber_tile.robber = True
                robber_tile.robber = False
                robber_moved = True

        return new_robber_tile

    def select_player_to_steal_from(self, player, able_to_steal_from: set) -> Player:
        select_player = InputHandler(
            value_range=list(able_to_steal_from),
            user=player.type,
            input_type="player",
            message=f"Choose a player to steal from {able_to_steal_from}: ",
            handler_backend=self.input_handler if hasattr(self.input_handler, "process") else None,
        ).process()

        robbed_player = [player for player in self.players if player.color in select_player and player.total_resources() > 0]
        if len(robbed_player) == 0:
            self.display_handler.message("No players to steal from.")

        return robbed_player

    def steal_random_resource(self, robbed_player: Player, current_player: Player) -> None:
        robbed_player = robbed_player[0]

        # Get the available resources of the robbed player
        available_resources = [
            resource_name.lower()
            for resource_name, resource in robbed_player.resources.__dict__.items()
            if isinstance(resource, TYPES) and resource.count > 0
        ]

        # Choose a random resource to steal
        random_resource = random.choice(list(available_resources))

        # Update the resource counts for the current player and the robbed player
        robbed_player.resources[random_resource].count -= 1
        current_player.resources[random_resource].count += 1

        self.display_handler.message(f"{current_player.color} stole {random_resource} from {robbed_player.color}.")

    def determine_who_to_steal_from(self, current_player: Player, new_robber_tile: Tile) -> Player:
        adjacent_nodes = new_robber_tile.get_near_nodes()

        able_to_steal_from = set()
        for node in adjacent_nodes:
            if isinstance(self.board.nodes[node].building, (Settlement, City)):
                able_to_steal_from.add(self.board.nodes[node].building.color)

        if current_player.color in able_to_steal_from:
            able_to_steal_from.remove(current_player.color)

        if len(able_to_steal_from) == 0:
            self.display_handler.message("No players to steal from.")

        return able_to_steal_from

    def robber_discard_resources(self) -> None:
        for player in self.players:
            total = player.total_resources()
            if total > 7:
                player.discard_resources(total)

    def limit_turn_options(self, player: Player) -> List[int]:
        all_options = [1, 2, 3, 4]

        can_build_road = True
        if player.resources.brick.count < 1 or player.resources.wood.count < 1:
            can_build_road = False

        can_build_settlement = True
        if (
            player.resources.brick.count < 1
            or player.resources.wood.count < 1
            or player.resources.wheat.count < 1
            or player.resources.sheep.count < 1
        ):
            can_build_settlement = False

        can_build_dev_card = True
        if player.resources.ore.count < 1 or player.resources.wheat.count < 1 or player.resources.sheep.count < 1:
            can_build_dev_card = False

        can_build_city = True
        if player.resources.ore.count < 2 or player.resources.wheat.count < 3:
            can_build_city = False

        if not any([can_build_road, can_build_settlement, can_build_dev_card, can_build_city]):
            all_options.remove(1)

        if (
            player.resources.brick.count < 1
            and player.resources.wood.count < 1
            and player.resources.wheat.count < 1
            and player.resources.sheep.count < 1
            and player.resources.ore.count < 1
        ):
            all_options.remove(2)

        dev_cards_to_play = [card for card in player.cards if card.played is False]
        if not can_build_dev_card and not dev_cards_to_play:
            all_options.remove(3)

        return all_options
