from dataclasses import dataclass

from src.core.board import Board


@dataclass
class Game:
    players: list
    board: Board

    def run():
        ...
