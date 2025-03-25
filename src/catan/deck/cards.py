from dataclasses import dataclass


@dataclass
class Knight:
    """
    Represents a Knight card in the Catan game.

    Attributes:
        color (str or None): The color of the player who owns the card.
        played (bool): Indicates whether the card has been played.
        player (str or None): The name of the player who owns the card.
    """

    color: str | None = None
    played: bool = False
    player: str | None = None

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class VictoryPoint:
    """
    Represents a victory point card in the Catan game.

    Attributes:
        color (str or None): The color of the player who owns the card.
        played (bool): Indicates whether the card has been played.
        player (str or None): The name of the player who owns the card.
    """

    color: str | None = None
    played: bool = False
    player: str | None = None

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class Monopoly:
    """
    Represents a Monopoly card in the Catan game.

    Attributes:
        color (str or None): The player color associated with the Monopoly card.
        played (bool): Indicates whether the Monopoly card has been played.
        player (str or None): The player who owns the Monopoly card.
    """

    color: str | None = None
    played: bool = False
    player: str | None = None

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class RoadBuilding:
    """
    Represents a Road Building card in the Catan game.

    Attributes:
        color (str or None): The color of the player who owns the card.
        played (bool): Indicates whether the card has been played.
        player (str or None): The name of the player who owns the card.
    """

    color: str | None = None
    played: bool = False
    player: str | None = None

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class YearOfPlenty:
    """
    Represents a Year of Plenty card in the Catan game.

    Attributes:
        color (str or None): The color of the card.
        played (bool): Indicates whether the card has been played.
        player (str or None): The player who owns the card.
    """

    color: str | None = None
    played: bool = False
    player: str | None = None

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value
