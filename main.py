from src.board.board import Board
from src.build.buildings import Buildings, Settlement
from src.game import Game
from src.player import Player

if __name__ == "__main__":
    board = Board()
    board.generate()
    game = Game(
        players=[
            Player(
                name="A",
                type="Human",
                color="Red",
                score=2,
                buildings=Buildings(
                    settlements=[
                        Settlement(color="Red", id=12),
                        Settlement(color="Red", id=15),
                    ]
                ),
            ),
            Player(
                name="B",
                color="Orange",
                score=2,
                buildings=Buildings(
                    settlements=[
                        Settlement(color="Red", id=19),
                        Settlement(color="Red", id=24),
                    ]
                ),
            ),
            Player(
                name="C",
                color="Blue",
                score=2,
                buildings=Buildings(
                    settlements=[
                        Settlement(color="Red", id=33),
                        Settlement(color="Red", id=41),
                    ]
                ),
            ),
            Player(
                name="D",
                color="White",
                score=2,
                buildings=Buildings(
                    settlements=[
                        Settlement(color="Red", id=37),
                        Settlement(color="Red", id=45),
                    ]
                ),
            ),
        ],
        board=board,
    )
    game.run()
