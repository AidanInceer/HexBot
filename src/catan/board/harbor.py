from dataclasses import dataclass
from typing import List

from src.catan.board.mapping import harbor_mapping


@dataclass
class Harbor:
    def __init__(self, id: int, resource: str, rate: int):
        """
        Initializes a Harbor object.

        Args:
            id (int): The ID of the harbor.
            resource (str): The resource associated with the harbor.
            rate (int): The trade rate of the harbor.

        Attributes:
            id (int): The ID of the harbor.
            resource (str): The resource associated with the harbor.
            rate (int): The trade rate of the harbor.
            nodes (List[int]): The list of adjacent nodes to the harbor.
        """
        self.id: int = id
        self.resource: str = resource
        self.rate: int = rate
        self.nodes: List[int] = harbor_mapping[self.id]["adjacent_nodes"]

    def near_nodes(self) -> List[int]:
        """
        Returns the list of adjacent nodes to the harbor.

        Returns:
            List[int]: The list of adjacent nodes.
        """
        return self.nodes

    def type(self) -> str:
        """
        Returns the resource associated with the harbor.

        Returns:
            str: The resource associated with the harbor.
        """
        return self.resource

    def trade_rate(self) -> int:
        """
        Returns the trade rate of the harbor.

        Returns:
            int: The trade rate of the harbor.
        """
        return self.rate

    def display_harbor(self) -> str:
        """
        Returns a string representation of the harbor.

        Returns:
            str: The string representation of the harbor.
        """
        return f"[{self.resource} {self.rate}:1]"
