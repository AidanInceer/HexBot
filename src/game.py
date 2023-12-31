from dataclasses import dataclass, field

from src.board.board import Board
from src.player import Player


@dataclass
class Game:
    players: list[Player]
    board: Board = field(default_factory=Board)
    game_ended: bool = False

    def run(self):
        while not self.game_ended:
            for player in self.players:
                self.turn(player)
                self.check_win()

    def check_win(self):
        for player in self.players:
            if player.score == 10:
                self.game_ended = True
                print(f"{player.color} won!")
                break

    def turn(self, player: Player):
        self.turn_ended = False
        print("=========================")
        print(f"{player.color}'s turn")
        print(
            f"Score: {player.score}, "
            f"Cards: {player.cards}, "
            f"Resources: {player.resources.resources}"
        )
        print("--------------------------")
        roll = player.roll()

        self.collect(roll)

        while not self.turn_ended:
            choice = input("1=Build, 2=Trade, 3=End: ")
            if choice == "1":
                player.build()
            elif choice == "2":
                player.trade()
            elif choice == "3":
                self.turn_ended = True

    def collect(self, roll: int):
        for player in self.players:
            active_tiles = self.board.active_tiles(roll)
            for tile in active_tiles:
                player.resources[tile] += 1
