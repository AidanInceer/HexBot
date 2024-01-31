from dataclasses import dataclass, field
from typing import List


@dataclass
class Settlement:
    """
    Represents a settlement in the game of Catan.

    Attributes:
        color (str): The color of the settlement.
        id (int): The unique identifier of the settlement.
    """

    color: str
    id: int


@dataclass
class City:
    """
    Represents a city in the game of Catan.

    Attributes:
        color (str): The color of the city.
        id (int): The unique identifier of the city.
    """

    color: str
    id: int


@dataclass
class Road:
    """
    Represents a road in the game of Catan.

    Attributes:
        color (str): The color of the road.
        id (int): The unique identifier of the road.
    """

    color: str
    id: int


@dataclass
class Buildings:
    """
    Represents the collection of buildings in the game.

    Attributes:
        settlements (List[Settlement]): A list of settlements.
        cities (List[City]): A list of cities.
        roads (List[Road]): A list of roads.
    """

    settlements: List[Settlement] = field(default_factory=list)
    cities: List[City] = field(default_factory=list)
    roads: List[Road] = field(default_factory=list)
