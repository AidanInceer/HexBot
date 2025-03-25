from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List

from src.catan.board.board import Board
from src.catan.buildings.buildings import Buildings
from src.catan.deck.cards import (
    Knight,
    Monopoly,
    RoadBuilding,
    VictoryPoint,
    YearOfPlenty,
)
from src.catan.deck.deck import CardDeck
from src.catan.game.setup.auto_setup import setup
from src.catan.player.managers.building_manager import BuildingManager
from src.catan.player.managers.development_card_manager import DevelopmentCardManager
from src.catan.player.managers.resource_manager import ResourceManager
from src.catan.player.managers.road_manager import RoadManager
from src.catan.player.managers.trade_manager import TradeManager
from src.catan.resources.resources import Resources
from src.interface.input_handler import InputHandler


@dataclass
class Player:
    """
    Represents a player in the game of Catan.

    Attributes:
        name (None | int): The name or identifier of the player.
        color (None | str): The color associated with the player.
        score (int): The current score of the player.
        type (None | str): The type or role of the player.
        buildings (Buildings): The buildings owned by the player.
        resources (Resources): The resources owned by the player.
        cards (List[Knight | VictoryPoint | Monopoly | RoadBuilding | YearOfPlenty]): The development cards owned by the player.
        longest_road (bool): Indicates if the player has the longest road.
        largest_army (bool): Indicates if the player has the largest army.
        knights_played (int): The number of knight cards played by the player.
    """

    name: None | int = None
    color: None | str = None
    score: int = 0
    type: None | str = None
    buildings: Buildings = field(default_factory=Buildings)
    resources: Resources = field(default_factory=Resources)
    cards: List[Knight | VictoryPoint | Monopoly | RoadBuilding | YearOfPlenty] = field(
        default_factory=list
    )
    longest_road: bool = False
    largest_army: bool = False
    knights_played: int = 0

    def __post_init__(self):
        """Initialize managers after the dataclass initialization."""
        # Initialize the resource manager
        self.resource_manager = ResourceManager(self.resources)
        
        # Initialize the building manager
        self.building_manager = BuildingManager(self, self.buildings)
        
        # Initialize the road manager
        self.road_manager = RoadManager()
        
        # Initialize the trade manager
        self.trade_manager = TradeManager(self)
        
        # Initialize the development card manager and sync cards
        self.dev_card_manager = DevelopmentCardManager(self)
        self.dev_card_manager.cards = self.cards  # Ensure cards are synced

    def roll(self) -> int:
        """
        Simulates rolling two dice and returns the sum of the two dice.

        Returns:
            int: The sum of the two dice rolls.
        """
        roll = random.randint(1, 6) + random.randint(1, 6)
        print(f"Roll: {roll}")
        return roll

    def build(
        self, board: Board, players: List[Player], setup: bool = False, auto=False
    ) -> None:
        """
        Builds settlements, cities, and roads for the player.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.
            setup (bool, optional): Indicates if it is the setup phase. Defaults to False.
            auto (bool, optional): Indicates if the building process is automated. Defaults to False.

        Returns:
            None
        """
        self.end_building = False
        while not self.end_building:
            if setup and auto:
                self.building_manager.build_settlement(board, players, auto=True)
                self.building_manager.build_road(board, players, self.road_manager, auto=True)
                self.end_building = True

            if setup and not auto:
                self.building_manager.build_settlement(board, players)
                board.display()
                self.building_manager.build_road(board, players, self.road_manager)
                board.display()
                self.end_building = True

            if not setup:
                choice = InputHandler(
                    value_range=[1, 2, 3, 4],
                    user=self.type,
                    input_type="action",
                    message="1=Settlement, 2=City, 3=Road, 4=End: ",
                ).process()
                if choice == 1:
                    self.building_manager.build_settlement(board, players)
                elif choice == 2:
                    self.building_manager.build_city(board, players)
                elif choice == 3:
                    self.building_manager.build_road(board, players, self.road_manager)
                elif choice == 4:
                    self.end_building = True

    def trade(self, board: Board, players: List[Player]) -> None:
        """
        Perform a trade action.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            None
        """
        self.trade_manager.trade(board, players)

    def dev_card(self, board: Board, players: List[Player], deck: CardDeck) -> None:
        """
        Allows the player to interact with development cards.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.
            deck (CardDeck): The deck of development cards.
        """
        self.dev_card_manager.dev_card(board, players, deck)

    def total_resources(self) -> int:
        """
        Calculate the total number of resources owned by the player.

        Returns:
            int: The total number of resources owned by the player.
        """
        return self.resource_manager.total_resources()

    def discard_resources(self, total: int) -> None:
        """
        Discard resources from the player's inventory when having too many cards during a 7 roll.

        Args:
            total (int): The total number of resources to be discarded.

        Returns:
            None
        """
        self.resource_manager.discard_resources(total)

    def __hash__(self):
        """
        Calculate the hash value of the player object.

        Returns:
            int: The hash value of the player object.
        """
        return hash(self.name)
