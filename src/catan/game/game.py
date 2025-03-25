import random
from dataclasses import dataclass, field

from src.catan.board.board import Board
from src.catan.board.tile import Tile
from src.catan.buildings.buildings import City, Settlement
from src.catan.deck.deck import CardDeck
from src.catan.player.player import Player
from src.catan.resources.resources import Brick, Ore, Sheep, Wheat, Wood
from src.catan.game.robber.robber_manager import RobberManager
from src.config.config import CentralConfig
from src.interface.input_handler import InputHandler

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

    def __post_init__(self):
        self.robber_manager = RobberManager(self.board, self.players)

    def run(self) -> None:
        """
        Runs the game loop until the game ends.
        """
        self.board.display()
        if self.game_type in [self.config.options.auto_types]:
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
        self.board.display()

    def game_setup(self) -> None:
        """
        Performs the game setup phase where each player takes turns to set up their initial settlements and roads.
        """

        for player in self.players:
            print(f"{player.color}'s turn to setup")
            player.build(self.board, self.players, setup=True, auto=False)

        for player in self.players[::-1]:
            print(f"{player.color}'s turn to setup")
            player.build(self.board, self.players, setup=True, auto=False)

    def check_win(self) -> None:
        """
        Checks if any player has reached a score of 10 and ends the game if so.
        """
        for player in self.players:
            if player.score == 10:
                self.game_ended = True
                print(f"{player.color} won!")
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
        self.board.display()

        roll = player.roll()
        if roll == 7:
            self.activate_robber(player)

        self.collect(roll)

        print(
            f"{player.color}'s turn   Score: {player.score} LR:{player.longest_road} LA:{player.largest_army}  Cards: {player.cards}   {player.resources}  \n"
            "==========================================================================================="
        )

        while not self.turn_ended:
            choice = InputHandler(
                value_range=[1, 2, 3, 4],
                user=player.type,
                input_type="int",
                message="1=Build, 2=Trade, 3=Dev Cards(Play/Select), 4=End: ",
            ).process()
            if choice == 1:
                player.build(self.board, self.players, setup=False, auto=False)
            elif choice == 2:
                player.trade(self.board, self.players)
            elif choice == 3:
                player.dev_card(self.board, self.deck, self.players)
            elif choice == 4:
                self.turn_ended = True

    def collect(self, roll: int) -> None:
        """
        Collect resources from settlements and cities on active tiles for each player.

        Args:
            roll (int): The roll of the dice.

        Returns:
            None
        """
        for player in self.players:
            active_tiles = [
                tile for tile in self.board.active_tiles(roll) if not tile.robber
            ]

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
            print(f"{player.color} collected {tile.type.produces}.")

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
            print(f"{player.color} collected {tile.type.produces}.")

    def activate_robber(self, current_player: Player) -> None:
        """
        Activates the robber and allows the current player to move it to a different tile.
        If there are adjacent players with resources, the current player can steal a random resource from one of them.
        If any player has more than 7 cards, they must discard half of their resources.

        Parameters:
            current_player (Player): The current player who activated the robber.

        Returns:
            None
        """
        self.robber_manager.activate_robber(current_player)
