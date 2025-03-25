from dataclasses import dataclass


@dataclass
class Hills:
    """
    Represents a hills terrain in the game of Catan.

    Attributes:
        name (str): The name of the terrain.
        produces (str): The resource produced by the terrain.
    """

    name: str = "Hills"
    produces: str = "brick"


@dataclass
class Forest:
    """
    Represents a forest terrain in the game of Catan.

    Attributes:
        name (str): The name of the terrain.
        produces (str): The resource produced by the terrain.
    """

    name: str = "Forest"
    produces: str = "wood"


@dataclass
class Mountains:
    """
    Represents a mountains terrain in the game of Catan.

    Attributes:
        name (str): The name of the terrain.
        produces (str): The resource produced by the terrain.
    """

    name: str = "Mountains"
    produces: str = "ore"


@dataclass
class Pasture:
    """
    Represents a pasture terrain in the game of Catan.

    Attributes:
        name (str): The name of the terrain.
        produces (str): The resource produced by the terrain.
    """

    name: str = "Pasture"
    produces: str = "sheep"


@dataclass
class Fields:
    """
    Represents a fields terrain in the game of Catan.

    Attributes:
        name (str): The name of the terrain.
        produces (str): The resource produced by the terrain.
    """

    name: str = "Fields"
    produces: str = "wheat"


@dataclass
class Desert:
    """
    Represents a desert terrain in the game of Catan.

    Attributes:
        name (str): The name of the terrain.
        produces (str): The resource produced by the terrain.
    """

    name: str = "Desert"
    produces: str = ""
