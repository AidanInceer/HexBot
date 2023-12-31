from src.board.board import Board
from src.game import Game
from src.player import Player

if __name__ == "__main__":
    board = Board()
    board.generate()
    game = Game(
        players=[
            Player(name="A", type="Human", color="Red"),
            Player(name="B", color="Orange"),
            Player(name="C", color="Blue"),
            Player(name="D", color="White"),
        ],
        board=board,
    )
    game.run()
