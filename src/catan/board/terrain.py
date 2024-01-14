from dataclasses import dataclass


@dataclass
class Hills:
    name: str = "Hills"
    produces: str = "brick"


@dataclass
class Forest:
    name: str = "Forest"
    produces: str = "wood"


@dataclass
class Mountains:
    name: str = "Mountains"
    produces: str = "ore"


@dataclass
class Pasture:
    name: str = "Pasture"
    produces: str = "sheep"


@dataclass
class Fields:
    name: str = "Fields"
    produces: str = "wheat"


@dataclass
class Desert:
    name: str = "Desert"
    produces: str = ""
