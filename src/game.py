from dataclasses import dataclass, field

from src.board.board import Board
from src.board.tile import Tile
from src.player import Player


@dataclass
class Game:
    players: list[Player]
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

        for player in self.players[::-1]:
            print(f"{player.color}'s turn to setup")
            player.build(self.board, setup=True)

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

        self.collect(roll)

        while not self.turn_ended:
            choice = input("1=Build, 2=Trade, 3=End: ")
            if choice == "1":
                player.build(self.board)
            elif choice == "2":
                player.trade(self.board)
            elif choice == "3":
                self.turn_ended = True

    def collect(self, roll: int):
        for player in self.players:
            active_tiles = self.board.active_tiles(roll)

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
