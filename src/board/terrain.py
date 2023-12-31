from dataclasses import dataclass


@dataclass
class Hills:
    produces: str = "brick"


@dataclass
class Forest:
    produces: str = "wood"


@dataclass
class Mountains:
    produces: str = "ore"


@dataclass
class Pasture:
    produces: str = "sheep"


@dataclass
class Fields:
    produces: str = "wheat"


@dataclass
class Desert:
    produces: str = ""
