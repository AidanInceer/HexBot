from dataclasses import dataclass
from typing import List, Union

from colorama import Fore

from src.catan.board.mapping import node_mapping
from src.catan.buildings.buildings import City, Settlement


@dataclass
class Node:
    def __init__(self, id):
        """
        Initialize a Node object.

        Args:
            id (int): The ID of the node.

        Attributes:
            id (int): The ID of the node.
            nodes (List[int]): List of IDs of adjacent nodes.
            edges (List[int]): List of IDs of adjacent edges.
            harbors (List[int]): List of IDs of adjacent harbors.
            tiles (List[int]): List of IDs of adjacent tiles.
            occupied (bool): Indicates if the node is occupied by a building.
            building (Union[None, Settlement, City]): The building on the node, if any.
            color (Union[None, str]): The color associated with the node, if any.
        """
        self.id: int = id
        self.nodes: List[int] = node_mapping[self.id]["adjacent_nodes"]
        self.edges: List[int] = node_mapping[self.id]["adjacent_edges"]
        self.harbors: List[int] = node_mapping[self.id]["adjacent_harbor"]
        self.tiles: List[int] = node_mapping[self.id]["adjacent_tiles"]
        self.occupied: bool = False
        self.building: Union[None, Settlement, City] = None
        self.color: Union[None, str] = None

    def near_nodes(self) -> List[int]:
        """
        Get the IDs of nodes adjacent to this node.

        Returns:
            List[int]: List of IDs of adjacent nodes.
        """
        return self.nodes

    def near_edges(self) -> List[int]:
        """
        Get the IDs of edges adjacent to this node.

        Returns:
            List[int]: List of IDs of adjacent edges.
        """
        return self.edges

    def near_harbors(self) -> List[int]:
        """
        Get the IDs of harbors adjacent to this node.

        Returns:
            List[int]: List of IDs of adjacent harbors.
        """
        return self.harbors

    def near_tiles(self) -> List[int]:
        """
        Get the IDs of tiles adjacent to this node.

        Returns:
            List[int]: List of IDs of adjacent tiles.
        """
        return self.tiles

    def display_node(self) -> str:
        """
        Get the string representation of the node.

        Returns:
            str: The string representation of the node.
        """
        if self.color == "Red":
            output = f"{Fore.RED + '(' + str(self.id).zfill(2) +')' + Fore.RESET}"
        elif self.color == "Blue":
            output = f"{Fore.BLUE + '(' + str(self.id).zfill(2) +')' + Fore.RESET}"
        elif self.color == "Green":
            output = f"{Fore.GREEN + '(' + str(self.id).zfill(2) +')' + Fore.RESET}"
        elif self.color == "Yellow":
            output = f"{Fore.YELLOW + '(' + str(self.id).zfill(2) +')' + Fore.RESET}"
        else:
            output = f"{'(' + str(self.id).zfill(2) +')'}"
        return output
