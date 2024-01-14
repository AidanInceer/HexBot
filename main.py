from src.catan.board.board import Board
from src.catan.deck.deck import CardDeck
from src.catan.game.game import Game
from src.catan.player.player import Player
from src.config.config import load_config
from src.utils.handlers import PathHandler

if __name__ == "__main__":
    config = load_config(PathHandler.config_path)

    deck = CardDeck()

    board = Board()
    board.generate()

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
        game_type=config.game_type,
        config=config,
    )
    game.run()
