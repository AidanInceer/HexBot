import random
from typing import List

from src.catan.deck.cards import (
    Knight,
    Monopoly,
    RoadBuilding,
    VictoryPoint,
    YearOfPlenty,
)


class CardDeck:
    def __init__(
        self,
    ) -> List[Knight | Monopoly | RoadBuilding | VictoryPoint | YearOfPlenty]:
        self.dev_cards = self.generate_dev_cards()

    def generate_dev_cards(
        self,
    ) -> List[Knight | Monopoly | RoadBuilding | VictoryPoint | YearOfPlenty]:
        self.dev_cards = [
            Knight(),
            Knight(),
            Knight(),
            Knight(),
            Knight(),
            Knight(),
            Knight(),
            Knight(),
            Knight(),
            Knight(),
            Knight(),
            Knight(),
            Knight(),
            Knight(),
            RoadBuilding(),
            RoadBuilding(),
            VictoryPoint(),
            VictoryPoint(),
            VictoryPoint(),
            VictoryPoint(),
            VictoryPoint(),
            YearOfPlenty(),
            YearOfPlenty(),
            Monopoly(),
            Monopoly(),
        ]

        random.shuffle(self.dev_cards)
        return self.dev_cards

    def select_dev_card(
        self,
    ) -> Knight | Monopoly | RoadBuilding | VictoryPoint | YearOfPlenty | None:
        if len(self.dev_cards) == 0:
            return None
        selected = self.dev_cards[0]
        self.dev_cards.pop(0)
        return selected
