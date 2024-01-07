from src.board.board import Board
from src.deck import CardDeck
from src.game import Game
from src.player import Player

if __name__ == "__main__":
    board = Board()
    board.generate()
    deck = CardDeck()
    game = Game(
        players=[
            Player(
                name="A",
                color="Red",
            ),
            Player(
                name="B",
                color="Orange",
            ),
            Player(
                name="C",
                color="Blue",
            ),
            Player(
                name="D",
                color="Green",
            ),
        ],
        deck=deck,
        board=board,
    )
    game.run()
