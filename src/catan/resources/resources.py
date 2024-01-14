from dataclasses import dataclass
from typing import List, Union


@dataclass
class Brick:
    """
    Represents a brick resource.

    Attributes:
        count (int): The number of brick resources.
        type (str): The type of resource, which is "brick".
    """

    count: int = 0
    type: str = "brick"

    def __str__(self) -> str:
        return str(self.count)


@dataclass
class Ore:
    """
    Represents an ore resource.

    Attributes:
        count (int): The number of ore resources.
        type (str): The type of resource, which is "ore".
    """

    count: int = 0
    type: str = "ore"

    def __str__(self) -> str:
        return str(self.count)


@dataclass
class Sheep:
    """
    Represents a sheep resource.

    Attributes:
        count (int): The number of sheep resources.
        type (str): The type of resource, which is "sheep".
    """

    count: int = 0
    type: str = "sheep"

    def __str__(self) -> str:
        return str(self.count)


@dataclass
class Wheat:
    """
    Represents a wheat resource.

    Attributes:
        count (int): The number of wheat resources.
        type (str): The type of resource, which is "wheat".
    """

    count: int = 0
    type: str = "wheat"

    def __str__(self) -> str:
        return str(self.count)


@dataclass
class Wood:
    """
    Represents a wood resource.

    Attributes:
        count (int): The number of wood resources.
        type (str): The type of resource, which is "wood".
    """

    count: int = 0
    type: str = "wood"

    def __str__(self) -> str:
        return str(self.count)


class Resources:
    """
    Represents a collection of resources in the game.
    """

    def __init__(self) -> None:
        self.brick: Brick = Brick(count=4)
        self.ore: Ore = Ore(count=0)
        self.sheep: Sheep = Sheep(count=2)
        self.wheat: Wheat = Wheat(count=2)
        self.wood: Wood = Wood(count=4)

    def __repr__(self) -> str:
        """
        Returns a string representation of the resources.

        Returns:
            str: A string representation of the resources.
        """
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
        """
        Increases the count of a specific resource.

        Args:
            resource (Union[Brick, Ore, Sheep, Wheat, Wood]): The resource to increase the count of.
        """
        self[resource].count += 1

    def __getitem__(self, key) -> Union[Brick, Ore, Sheep, Wheat, Wood]:
        """
        Returns the resource with the specified key.

        Args:
            key: The key of the resource.

        Returns:
            Union[Brick, Ore, Sheep, Wheat, Wood]: The resource with the specified key.
        """
        return self.__dict__.get(key)

    def __setitem__(self, key, value) -> None:
        """
        Sets the value of the resource with the specified key.

        Args:
            key: The key of the resource.
            value: The value to set.
        """
        self[key] = value

    def all_resources(self) -> List[str]:
        """
        Returns a list of all resource types.

        Returns:
            List[str]: A list of all resource types.
        """
        return [
            self.brick.type,
            self.ore.type,
            self.sheep.type,
            self.wheat.type,
            self.wood.type,
        ]
