import unittest

from src.catan.deck.cards import (
    Knight,
    Monopoly,
    RoadBuilding,
    VictoryPoint,
    YearOfPlenty,
)
from src.catan.deck.deck import CardDeck


class TestCardDeck(unittest.TestCase):
    def setUp(self):
        self.card_deck = CardDeck()

    def test_generate_dev_cards(self):
        dev_cards = self.card_deck.generate_dev_cards()
        self.assertEqual(
            len(dev_cards), 25
        )  # Assuming there are 25 development cards in the deck

    def test_select_dev_card(self):
        dev_card = self.card_deck.select_dev_card()
        self.assertIsInstance(
            dev_card, (Knight, Monopoly, RoadBuilding, VictoryPoint, YearOfPlenty)
        )

    def test_empty_deck(self):
        # Test selecting a dev card from an empty deck
        self.card_deck.generate_dev_cards()  # Generate dev cards to ensure the deck is not empty
        for _ in range(25):
            self.card_deck.select_dev_card()  # Consume all dev cards
        actual = (
            self.card_deck.select_dev_card()
        )  # Attempt to select a dev card from an empty deck

        assert actual is None

    def test_shuffle_deck(self):
        # Test shuffling the deck and ensuring the order changes
        original_deck = self.card_deck.generate_dev_cards()
        shuffled_deck = self.card_deck.generate_dev_cards()
        self.assertNotEqual(
            original_deck, shuffled_deck
        )  # Check if the decks are different

    def test_specific_card_in_deck(self):
        # Test if a specific card is present in the deck after generating dev cards
        dev_cards = self.card_deck.generate_dev_cards()
        self.assertIn(
            Knight(), dev_cards
        )  # Assuming Knight card is one of the possible dev cards
