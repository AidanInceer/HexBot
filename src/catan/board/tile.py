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
        """
        Initialize a Tile object.

        Args:
            type: The type of the tile.
            id: The ID of the tile.
            robber: Whether the tile has a robber or not.
        """
        self.type: Desert | Fields | Forest | Hills | Mountains | Pasture = type
        self.id: int = id
        self.token: None | int = None
        self.nodes: List[int] = tile_mapping[self.id]["adjacent_nodes"]
        self.robber: bool = robber

    def __repr__(self) -> str:
        """
        Return a string representation of the Tile object.

        Returns:
            A string representation of the Tile object.
        """
        return f"Tile(type={self.type.name}, id={self.id}, token={self.token}, nodes={self.nodes}, robber={self.robber})"

    def get_near_nodes(self) -> List[int]:
        """
        Get the IDs of the nodes adjacent to the tile.

        Returns:
            A list of IDs of the nodes adjacent to the tile.
        """
        return self.nodes

    def tile(self) -> Desert | Fields | Forest | Hills | Mountains | Pasture:
        """
        Get the type of the tile.

        Returns:
            The type of the tile.
        """
        return self.type

    def value(self) -> int:
        """
        Get the token value of the tile.

        Returns:
            The token value of the tile.
        """
        return self.token

    def display_type(self) -> str:
        """
        Get the formatted display type of the tile.

        Returns:
            The formatted display type of the tile.
        """
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
        """
        Get the formatted display token of the tile.

        Returns:
            The formatted display token of the tile.
        """
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
        """
        Check if the tile has a robber.

        Returns:
            True if the tile has a robber, False otherwise.
        """
        return self.robber

    def display_id(self):
        """
        Get the formatted display ID of the tile.

        Returns:
            The formatted display ID of the tile.
        """
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
        """
        Get the formatted display pips of the tile.

        Returns:
            The formatted display pips of the tile.
        """
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
        """
        Get the formatted display robber of the tile.

        Returns:
            The formatted display robber of the tile.
        """
        if self.robber:
            output = "(R)"
        else:
            output = "   "
        return output
