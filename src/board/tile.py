from dataclasses import dataclass
from typing import List, Union

from colorama import Fore

from src.board.mapping import tile_mapping
from src.board.terrain import Desert, Fields, Forest, Hills, Mountains, Pasture

DESERT_COLOR = "\033[38;5;214m"
FIELDS_COLOR = "\033[38;5;190m"
FOREST_COLOR = "\033[38;5;02m"
PASTURE_COLOR = "\033[38;5;40m"
HILLS_COLOR = Fore.LIGHTRED_EX
MOUNTAINS_COLOR = Fore.LIGHTBLACK_EX


@dataclass
class Tile:
    def __init__(self, type, id, robber=False):
        self.type: Union[Desert, Fields, Forest, Hills, Mountains, Pasture] = type
        self.id: int = id
        self.token: Union[None, int] = None
        self.nodes: List[int] = tile_mapping[self.id]["adjacent_nodes"]
        self.robber: bool = robber

    def __repr__(self) -> str:
        return f"Tile(name={self.type.name}, id={self.id}, token={self.token}, nodes={self.nodes})"

    def get_near_nodes(self):
        return self.nodes

    def tile(self):
        return self.type

    def value(self):
        return self.token

    def display_type(self):
        if isinstance(self.type, Desert):
            output = f"{DESERT_COLOR + self.type.name[:4].upper() + Fore.RESET}"
        elif isinstance(self.type, Fields):
            output = f"{FIELDS_COLOR + self.type.name[:4].upper() + Fore.RESET}"
        elif isinstance(self.type, Forest):
            output = f"{FOREST_COLOR + self.type.name[:4].upper() + Fore.RESET}"
        elif isinstance(self.type, Pasture):
            output = f"{PASTURE_COLOR + self.type.name[:4].upper() + Fore.RESET}"
        elif isinstance(self.type, Hills):
            output = f"{HILLS_COLOR + self.type.name[:4].upper() + Fore.RESET}"
        elif isinstance(self.type, Mountains):
            output = f"{MOUNTAINS_COLOR + self.type.name[:4].upper() + Fore.RESET}"

        return output

    def display_token(self):
        token_check = "07" if self.token is None else str(self.token).zfill(2)
        if isinstance(self.type, Desert):
            output = f"{DESERT_COLOR + token_check + Fore.RESET}"
        elif isinstance(self.type, Fields):
            output = f"{FIELDS_COLOR + token_check + Fore.RESET}"
        elif isinstance(self.type, Forest):
            output = f"{FOREST_COLOR + token_check + Fore.RESET}"
        elif isinstance(self.type, Pasture):
            output = f"{PASTURE_COLOR + token_check + Fore.RESET}"
        elif isinstance(self.type, Hills):
            output = f"{HILLS_COLOR + token_check + Fore.RESET}"
        elif isinstance(self.type, Mountains):
            output = f"{MOUNTAINS_COLOR + token_check + Fore.RESET}"

        return output

    def has_robber(self):
        return self.robber

    def display_id(self):
        if isinstance(self.type, Desert):
            output = f"{DESERT_COLOR + str(self.id).zfill(2) + Fore.RESET}"
        elif isinstance(self.type, Fields):
            output = f"{FIELDS_COLOR + str(self.id).zfill(2) + Fore.RESET}"
        elif isinstance(self.type, Forest):
            output = f"{FOREST_COLOR + str(self.id).zfill(2) + Fore.RESET}"
        elif isinstance(self.type, Pasture):
            output = f"{PASTURE_COLOR + str(self.id).zfill(2) + Fore.RESET}"
        elif isinstance(self.type, Hills):
            output = f"{HILLS_COLOR + str(self.id).zfill(2) + Fore.RESET}"
        elif isinstance(self.type, Mountains):
            output = f"{MOUNTAINS_COLOR + str(self.id).zfill(2) + Fore.RESET}"

        return output

    def display_pips(self):
        mapping = {
            2: 1,
            3: 2,
            4: 3,
            5: 3,
            6: 4,
            7: 0,
            8: 4,
            9: 3,
            10: 3,
            11: 2,
            12: 1,
        }
        if self.token is None:
            pip = "  "
        else:
            pip = str(mapping[self.token]).zfill(2)

        if isinstance(self.type, Desert):
            output = f"{DESERT_COLOR + pip + Fore.RESET}"
        elif isinstance(self.type, Fields):
            output = f"{FIELDS_COLOR + pip + Fore.RESET}"
        elif isinstance(self.type, Forest):
            output = f"{FOREST_COLOR + pip + Fore.RESET}"
        elif isinstance(self.type, Pasture):
            output = f"{PASTURE_COLOR + pip + Fore.RESET}"
        elif isinstance(self.type, Hills):
            output = f"{HILLS_COLOR + pip + Fore.RESET}"
        elif isinstance(self.type, Mountains):
            output = f"{MOUNTAINS_COLOR + pip + Fore.RESET}"

        return output
