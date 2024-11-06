from src.catan.board.board import Board
from src.catan.deck.deck import CardDeck
from src.catan.game.game import Game
from src.catan.player.player import Player
from src.config.config import load_config
from src.utils.handlers import PathHandler
import time


if __name__ == "__main__":
    start_time = time.time()
    runs = 3
    for i in range(0,runs,1):
        config = load_config(PathHandler.config_path)

        deck = CardDeck().generate_dev_cards()

        board = Board()
        board.generate()

        game = Game(
            players=[
                Player(name=0, color="Red", type="bot"),
                Player(name=1, color="Yellow", type="bot"),
                Player(name=2, color="Blue", type="bot"),
                Player(name=3, color="Green", type="bot"),
            ],
            deck=deck,
            board=board,
            game_type="AUTO_SETUP",
            config=config,
        )
        game.run()
        time.sleep(2)
        print(i)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{runs} runs took {elapsed_time:.6f} seconds to run.")