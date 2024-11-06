from dataclasses import dataclass
from typing import List

from colorama import Fore

from src.catan.board.mapping import tile_mapping
from src.catan.board.terrain import Desert, Fields, Forest, Hills, Mountains, Pasture

DESERT_COLOR = "\033[38;5;214m"
FIELDS_COLOR = "\033[38;5;190m"
FOREST_COLOR = "\033[38;5;02m"
PASTURE_COLOR = "\033[38;5;40m"
HILLS_COLOR = Fore.LIGHTRED_EX
MOUNTAINS_COLOR = Fore.LIGHTBLACK_EX


@dataclass
class Tile:
    def __init__(self, type, id, robber=False):
        self.type: Desert | Fields | Forest | Hills | Mountains | Pasture = type
        self.id: int = id
        self.token: None | int = None
        self.nodes: List[int] = tile_mapping[self.id]["adjacent_nodes"]
        self.robber: bool = robber

    def __repr__(self) -> str:
        return f"Tile(type={self.type.name}, id={self.id}, token={self.token}, nodes={self.nodes}, robber={self.robber})"

    def get_near_nodes(self) -> List[int]:
        return self.nodes

    def tile(self) -> Desert | Fields | Forest | Hills | Mountains | Pasture:
        return self.type

    def value(self) -> int | None:
        return self.token

    def display_type(self) -> str:
        formatted = self.type.name.upper()

        if isinstance(self.type, Desert):
            output = f"{DESERT_COLOR} {formatted}  {Fore.RESET}"
        elif isinstance(self.type, Fields):
            output = f"{FIELDS_COLOR} {formatted}  {Fore.RESET}"
        elif isinstance(self.type, Forest):
            output = f"{FOREST_COLOR} {formatted}  {Fore.RESET}"
        elif isinstance(self.type, Pasture):
            output = f"{PASTURE_COLOR} {formatted} {Fore.RESET}"
        elif isinstance(self.type, Hills):
            output = f"{HILLS_COLOR}  {formatted}  {Fore.RESET}"
        elif isinstance(self.type, Mountains):
            output = f"{MOUNTAINS_COLOR}{formatted}{Fore.RESET}"

        return output

    def display_token(self) -> str:
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

    def has_robber(self) -> bool:
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

    def display_pips(self) -> str:
        mapping = {
            2: ".    ",
            3: "..   ",
            4: "...  ",
            5: ".... ",
            6: ".....",
            8: ".....",
            9: ".... ",
            10: "...  ",
            11: "..   ",
            12: ".    ",
        }
        if isinstance(self.type, Desert) and self.robber:
            pip = " (R) "
        elif isinstance(self.type, Desert):
            pip = "     "
        elif self.robber:
            pip = " (R) "
        else:
            pip = str(mapping[self.token])

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

    def display_robber(self) -> str:
        if self.robber:
            output = "(R)"
        else:
            output = "   "
        return output
