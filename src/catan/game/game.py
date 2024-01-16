import random
from dataclasses import dataclass, field

from src.catan.board.board import Board
from src.catan.board.tile import Tile
from src.catan.buildings.buildings import City, Settlement
from src.catan.deck.deck import CardDeck
from src.catan.player.player import Player
from src.catan.resources.resources import Brick, Ore, Sheep, Wheat, Wood
from src.config.config import CentralConfig


@dataclass
class Game:
    players: list[Player]
    deck: CardDeck
    game_type: str
    config: CentralConfig
    board: Board = field(default_factory=Board)
    game_ended: bool = False

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
            choice = input("1=Build, 2=Trade, 3=Dev Cards(Play/Select), 4=End: ")
            if choice == "1":
                player.build(self.board, self.players, setup=False, auto=False)
            elif choice == "2":
                player.trade(self.board, self.players)
            elif choice == "3":
                player.dev_card(self.board, self.deck, self.players)
            elif choice == "4":
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
        robber_tile = self.board.get_robber_tile()

        robber_moved = False
        while not robber_moved:
            move_robber = int(input("Choosen a Tile [0-18] to move the Robber to: "))
            if move_robber < 0 or move_robber > 18:
                print("Invalid tile.")
            elif move_robber == robber_tile.id:
                print("Robber must be moved to a different tile.")
            else:
                new_robber_tile = self.board.set_robber_tile(move_robber)
                new_robber_tile.robber = True
                robber_tile.robber = False
                robber_moved = True

        # choosen a player to steal a random resource from
        # if the player has no resources, they are skipped
        adjacent_nodes = new_robber_tile.get_near_nodes()

        able_to_steal_from = set()
        for node in adjacent_nodes:
            if isinstance(self.board.nodes[node].building, (Settlement, City)):
                able_to_steal_from.add(self.board.nodes[node].building.color)

        if current_player.color in able_to_steal_from:
            able_to_steal_from.remove(current_player.color)

        if len(able_to_steal_from) == 0:
            print("No players to steal from.")

        else:
            select_player = input(
                f"Choosen a player to steal from {able_to_steal_from}: "
            )

            robbed_player = [
                player
                for player in self.players
                if player.color in select_player and player.total_resources() > 0
            ]
            if len(robbed_player) == 0:
                print("No players to steal from.")
            else:
                robbed_player = robbed_player[0]
                types = (
                    Brick,
                    Ore,
                    Sheep,
                    Wheat,
                    Wood,
                )

                # Get the available resources of the robbed player
                available_resources = [
                    resource_name.lower()
                    for resource_name, resource in robbed_player.resources.__dict__.items()
                    if isinstance(resource, types) and resource.count > 0
                ]

                # Choose a random resource to steal
                random_resource = random.choice(list(available_resources))

                # Update the resource counts for the current player and the robbed player
                robbed_player.resources[random_resource].count -= 1
                current_player.resources[random_resource].count += 1

                print(
                    f"{current_player.color} stole {random_resource} from {robbed_player.color}."
                )

        # if any player has more than 7 cards, they must discard half
        for player in self.players:
            total = player.total_resources()
            if total > 7:
                player.discard_resources(total)
