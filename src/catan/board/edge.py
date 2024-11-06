from dataclasses import dataclass
from typing import List

from colorama import Fore

from src.catan.board.mapping import edge_mapping


@dataclass
class Edge:
    def __init__(self, id):
        self.id = id
        self.nodes: List[int] = edge_mapping[self.id]["adjacent_nodes"]
        self.edges: List[int] = edge_mapping[self.id]["adjacent_edges"]
        self.occupied: bool = False
        self.color: None | str = None

    def near_nodes(self) -> List[int]:
        return self.nodes

    def __hash__(self) -> int:
        return hash(str(self))

    def display_edge(self) -> str:
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
