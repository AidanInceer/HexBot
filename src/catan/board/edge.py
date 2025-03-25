from dataclasses import dataclass
from typing import List

from colorama import Fore

from src.catan.board.mapping import edge_mapping


@dataclass
class Edge:
    """Represents an edge on the Catan board."""

    def __init__(self, id):
        """
        Initializes an Edge object.

        Args:
            id (int): The ID of the edge.
        """
        self.id = id
        self.nodes: List[int] = edge_mapping[self.id]["adjacent_nodes"]
        self.edges: List[int] = edge_mapping[self.id]["adjacent_edges"]
        self.occupied: bool = False
        self.color: None | str = None

    def near_nodes(self) -> List[int]:
        """
        Returns a list of IDs of the nodes adjacent to the edge.

        Returns:
            List[int]: A list of node IDs.
        """
        return self.nodes

    def __hash__(self) -> int:
        """
        Returns the hash value of the Edge object.

        Returns:
            int: The hash value.
        """
        return hash(str(self))

    def display_edge(self) -> str:
        """
        Returns a string representation of the edge, including its ID and color.

        Returns:
            str: The string representation of the edge.
        """
        if self.color == "Red":
            output = f"{Fore.RED + str(self.id).zfill(2) + Fore.RESET}"
        elif self.color == "Blue":
            output = f"{Fore.BLUE + str(self.id).zfill(2) + Fore.RESET}"
        elif self.color == "Green":
            output = f"{Fore.GREEN + str(self.id).zfill(2) + Fore.RESET}"
        elif self.color == "Yellow":
            output = f"{Fore.YELLOW + str(self.id).zfill(2) + Fore.RESET}"
        else:
            output = f"{str(self.id).zfill(2)}"
        return output
