import random

from src.catan.deck.cards import (
    Knight,
    Monopoly,
    RoadBuilding,
    VictoryPoint,
    YearOfPlenty,
)


class CardDeck:
    """
    Represents a deck of development cards in the game of Catan.
    """

    def __init__(
        self,
    ) -> List[Knight | Monopoly | RoadBuilding | VictoryPoint | YearOfPlenty]:
        self.dev_cards = self.generate_dev_cards()

    def generate_dev_cards(
        self,
    ) -> List[List[Knight | Monopoly | RoadBuilding | VictoryPoint | YearOfPlenty]]:
        """
        Generates a list of development cards and shuffles them randomly.

        Returns:
            List[List[Knight | Monopoly | RoadBuilding | VictoryPoint | YearOfPlenty]]:
            A list of development cards.
        """
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
        """
        Selects a development card from the deck.

        Returns:
            List[Knight | Monopoly | RoadBuilding | VictoryPoint | YearOfPlenty]: The selected development card.
        """
        if len(self.dev_cards) == 0:
            return None
        selected = self.dev_cards[0]
        self.dev_cards.pop(0)
        return selected
