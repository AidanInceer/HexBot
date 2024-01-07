import random
from dataclasses import dataclass, field

from src.board.board import Board
from src.board.tile import Tile
from src.build.buildings import City, Settlement
from src.deck import CardDeck
from src.player import Player


@dataclass
class Game:
    players: list[Player]
    deck: CardDeck
    board: Board = field(default_factory=Board)
    game_ended: bool = False

    def run(self):
        self.board.display()
        self.game_setup()
        while not self.game_ended:
            for player in self.players:
                self.turn(player)
                self.check_win()

    def game_setup(self):
        for player in self.players:
            print(f"{player.color}'s turn to setup")
            player.build(self.board, setup=True)
            self.board.display()

        for player in self.players[::-1]:
            print(f"{player.color}'s turn to setup")
            player.build(self.board, setup=True)
            self.board.display()

    def check_win(self):
        for player in self.players:
            if player.score == 10:
                self.game_ended = True
                print(f"{player.color} won!")
                break

    def turn(self, player: Player):
        self.turn_ended = False
        self.board.display()
        print(
            f"| {player.color}'s turn | Score: {player.score} | {player.cards} | {player.resources}  |\n"
            "==========================================================================================="
        )
        roll = player.roll()
        if roll == 7:
            self.activate_robber(player)

        self.collect(roll)

        while not self.turn_ended:
            choice = input("1=Build, 2=Trade, 3=Dev Cards(Play/Select), 4=End: ")
            if choice == "1":
                player.build(self.board)
            elif choice == "2":
                player.trade(self.board)
            elif choice == "3":
                player.dev_card(self.board)
            elif choice == "4":
                self.turn_ended = True

    def collect(self, roll: int):
        for player in self.players:
            active_tiles = [
                tile for tile in self.board.active_tiles(roll) if not tile.robber
            ]

            for tile in active_tiles:
                self.collect_from_settlements(player, tile)
                self.collect_from_cities(player, tile)

    def collect_from_settlements(self, player: Player, tile: Tile):
        active_nodes = [settlement.id for settlement in player.buildings.settlements]
        tile_nodes = tile.nodes

        if any(node in active_nodes for node in tile_nodes):
            player.resources[tile.type.produces].count += 1
            print(f"{player.color} collected {tile.type.produces}.")

    def collect_from_cities(self, player: Player, tile: Tile):
        active_nodes = [city.id for city in player.buildings.cities]
        tile_nodes = tile.nodes

        if any(node in active_nodes for node in tile_nodes):
            player.resources[tile.type.produces].count += 2
            print(f"{player.color} collected {tile.type.produces}.")

    def activate_robber(self, current_player: Player):
        # move and update the robbber location
        robber_tile = self.board.get_robber_tile()

        robber_moved = False
        while not robber_moved:
            move_robber = int(input("Choosen a Tile [0-18] to move the Robber to: "))
            if move_robber == robber_tile.id:
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
                available_resources = [
                    str(res.__class__.__name__).lower()
                    for key, res in robbed_player.resources.__dict__.items()
                    if res.count > 0
                ]
                random_resource = random.choice(list(available_resources))

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
