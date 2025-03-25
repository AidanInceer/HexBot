from __future__ import annotations

from typing import List

from src.catan.board.board import Board
from src.catan.deck.cards import (
    Knight,
    Monopoly,
    RoadBuilding,
    VictoryPoint,
    YearOfPlenty,
)
from src.catan.deck.deck import CardDeck
from src.interface.input_handler import InputHandler


class DevelopmentCardManager:
    """Manages development cards for a player."""
    
    def __init__(self, player):
        self.player = player
        self.cards = []
    
    def dev_card(self, board: Board, players: List, deck: CardDeck) -> None:
        """
        Allows the player to interact with development cards.

        Args:
            board (Board): The game board.
            players (List): The list of players in the game.
            deck (CardDeck): The deck of development cards.
        """
        choice = InputHandler(
            value_range=[1, 2, 3],
            user=self.player.type,
            input_type="action",
            message="1=Collect dev card, 2=Play dev card, 3=End: ",
        ).process()
        if choice == 1:
            self.collect_dev_card(deck)
        elif choice == 2:
            self.select_dev_card_to_play(board, players)
        elif choice == 3:
            pass
    
    def collect_dev_card(self, deck: CardDeck) -> None:
        """
        Collects a development card from the given deck if the player has enough resources.

        Args:
            deck (CardDeck): The deck of development cards.

        Returns:
            None
        """
        # Only collect dev card if you have 1 wool, 1 grain, and 1 ore.
        if self.player.resource_manager.has_resources_for_dev_card():
            # Check if there are any cards left in the deck
            if len(deck.dev_cards) == 0:
                print("No development cards left in the deck")
                return
                
            # Remove the amount of resources needed for dev card.
            self.player.resource_manager.deduct_dev_card_cost()
            # Get a card from the deck
            card = deck.deal_card()
            # Add the card to the player's cards
            self.cards.append(card)
        else:
            print("Not enough resources to collect a development card")
    
    def select_dev_card_to_play(self, board: Board, players: List) -> None:
        """
        Allows the player to select a development card to play.

        Args:
            board (Board): The game board.
            players (List): The list of players in the game.

        Returns:
            None
        """
        # Display the cards the player has
        if len(self.cards) > 0:
            print("Development cards:")
            
            # Get the input for which card to play
            choice = InputHandler(
                value_range=range(1, len(self.cards) + 1),
                user=self.player.type,
                input_type="int",
                message="Select a card to play: ",
            ).process()
            
            # Play the card
            self.play_dev_card(self.cards[choice - 1], board, players)
        else:
            print("You have no development cards")
    
    def play_dev_card(
        self,
        card: Knight | VictoryPoint | Monopoly | RoadBuilding | YearOfPlenty,
        board: Board,
        players: List,
    ) -> None:
        """
        Plays a development card.

        Args:
            card (Knight | VictoryPoint | Monopoly | RoadBuilding | YearOfPlenty): The development card to be played.
            board (Board): The game board.
            players (List): The list of players in the game.

        Returns:
            None
        """
        # Remove the card from the player's hand
        self.cards.remove(card)
        
        # Play the card
        if isinstance(card, Knight):
            self.play_knight(board, players)
        elif isinstance(card, VictoryPoint):
            self.play_victory_point()
        elif isinstance(card, Monopoly):
            self.play_monopoly(players)
        elif isinstance(card, RoadBuilding):
            self.play_road_building(board, players)
        elif isinstance(card, YearOfPlenty):
            self.play_year_of_plenty()
    
    def play_knight(self, board: Board, players: List) -> None:
        """
        Activates the knight and checks if the player has the largest army.

        Args:
            board (Board): The game board.
            players (List): The list of players in the game.

        Returns:
            None
        """
        self.activate_knight(board, players)
        self.check_largest_army(players)
    
    def activate_knight(self, board: Board, players: List) -> None:
        """
        Activates a knight card for the player.

        Args:
            board (Board): The game board.
            players (List): The list of players in the game.

        Returns:
            None
        """
        self.player.knights_played += 1
        # Implementation details for activating knight
        pass
    
    def check_largest_army(self, players: List) -> None:
        """
        Checks if the current player has the largest army in the game and updates the scores accordingly.

        Args:
            players (List): A list of Player objects representing all the players in the game.

        Returns:
            None
        """
        # Find the player with the largest army (must be at least 3 knights)
        max_knights = 0
        max_player = None
        for player in players:
            if player.knights_played >= 3 and player.knights_played > max_knights:
                max_knights = player.knights_played
                max_player = player
        
        # Reset largest army status for all players
        for player in players:
            if player.largest_army:
                player.score -= 2
                player.largest_army = False
        
        # Assign largest army to the player with the largest army
        if max_player is not None:
            max_player.largest_army = True
            max_player.score += 2
    
    def play_victory_point(self) -> None:
        """
        Increases the player's score by 1 and prints a message indicating that a Victory Point card was played.

        Returns:
            None
        """
        self.player.score += 1
        print("You played a Victory Point card")
    
    def play_monopoly(self, players: List) -> None:
        """
        Monopolizes a specific resource from other players.

        Args:
            players (List): A list of Player objects representing the other players.

        Returns:
            None
        """
        # Implementation details for monopoly
        pass
    
    def play_road_building(self, board: Board, players: List) -> None:
        """
        Plays the Road Building development card.

        Args:
            board (Board): The game board.
            players (List): The list of players in the game.

        Returns:
            None
        """
        # Build two roads for free
        for _ in range(2):
            self.player.building_manager.build_road(board, players, self.player.road_manager, dev_card=True)
    
    def play_year_of_plenty(self) -> None:
        """
        Allows the player to collect two resources of their choice.

        This method prompts the player to input the names of two resources they would like to collect.
        The count of the chosen resources in the player's resources dictionary is then incremented by 1.

        Parameters:
            None

        Returns:
            None
        """
        # Implementation details for year of plenty
        pass
