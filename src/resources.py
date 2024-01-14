from dataclasses import dataclass
from typing import List, Union


@dataclass
class Brick:
    count: int = 0
    type: str = "brick"

    def __str__(self) -> str:
        return str(self.count)


@dataclass
class Ore:
    count: int = 0
    type: str = "ore"

    def __str__(self) -> str:
        return str(self.count)


@dataclass
class Sheep:
    count: int = 0
    type: str = "sheep"

    def __str__(self) -> str:
        return str(self.count)


@dataclass
class Wheat:
    count: int = 0
    type: str = "wheat"

    def __str__(self) -> str:
        return str(self.count)


@dataclass
class Wood:
    count: int = 0
    type: str = "wood"

    def __str__(self) -> str:
        return str(self.count)


class Resources:
    def __init__(self) -> None:
        self.brick: Brick = Brick(count=4)
        self.ore: Ore = Ore(count=0)
        self.sheep: Sheep = Sheep(count=2)
        self.wheat: Wheat = Wheat(count=2)
        self.wood: Wood = Wood(count=4)

    def __repr__(self) -> str:
        resources = []
        types = [
            "brick",
            "ore",
            "sheep",
            "wheat",
            "wood",
        ]
        for res in types:
            if getattr(self, res).count > 0:
                resources.append(f"{res}: {getattr(self, res)}")

        resources = ", ".join(resources)

        return f"Resources: {resources}"

    def set_attr(self, resource: Union[Brick, Ore, Sheep, Wheat, Wood]):
        self[resource].count += 1

    def __getitem__(self, key) -> Union[Brick, Ore, Sheep, Wheat, Wood]:
        return self.__dict__.get(key)

    def __setitem__(self, key, value) -> None:
        self[key] = value

    def all_resources(self) -> List[str]:
        return [
            self.brick.type,
            self.ore.type,
            self.sheep.type,
            self.wheat.type,
            self.wood.type,
        ]
