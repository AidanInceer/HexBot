from dataclasses import dataclass
from typing import List

from colorama import Fore

from src.catan.board.mapping import node_mapping
from src.catan.buildings.buildings import City, Settlement


@dataclass
class Node:
    def __init__(self, id):
        self.id: int = id
        self.nodes: List[int] = node_mapping[self.id]["adjacent_nodes"]
        self.edges: List[int] = node_mapping[self.id]["adjacent_edges"]
        self.harbors: List[int] = node_mapping[self.id]["adjacent_harbor"]
        self.tiles: List[int] = node_mapping[self.id]["adjacent_tiles"]
        self.occupied: bool = False
        self.building: None | Settlement | City = None
        self.color: None | str = None

    def near_nodes(self) -> List[int]:
        return self.nodes

    def near_edges(self) -> List[int]:
        return self.edges

    def near_harbors(self) -> List[int]:
        return self.harbors

    def near_tiles(self) -> List[int]:
        return self.tiles

    def display_node(self) -> str:
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
