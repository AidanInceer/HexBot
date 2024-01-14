from src.board.board import Board
from src.deck.deck import CardDeck
from src.game.game import Game
from src.game.types import GameTypes
from src.player.player import Player

if __name__ == "__main__":
    board = Board()
    board.generate()
    deck: CardDeck = CardDeck()
    game = Game(
        players=[
            Player(
                name=0,
                color="Red",
            ),
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
        ],
        deck=deck,
        board=board,
        game_type=GameTypes.AUTO_SETUP,
    )
    game.run()
