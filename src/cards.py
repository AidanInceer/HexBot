from dataclasses import dataclass
from typing import Union


@dataclass
class Knight:
    color: Union[str, None] = None
    played: bool = False
    player: Union[str, None] = None

    def play(self, board):
        self.played = True
        print("Played Knight")
        # TODO: Move the robber
        # TODO: Steal a card from another player

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class VictoryPoint:
    color: Union[str, None] = None
    played: bool = False
    player: Union[str, None] = None

    def play(self, board):
        self.played = True
        print("Played Victory Point")
        # TODO: Add a victory point to the player

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class Monopoly:
    color: Union[str, None] = None
    played: bool = False
    player: Union[str, None] = None

    def play(self, board):
        self.played = True
        print("Played Monopoly")
        # TODO: Steal all of a certain resource from other players

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class RoadBuilding:
    color: Union[str, None] = None
    played: bool = False
    player: Union[str, None] = None

    def play(self, board):
        self.played = True
        print("Played Road Building")
        # TODO: Build two roads for free

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class YearOfPlenty:
    color: Union[str, None] = None
    played: bool = False
    player: Union[str, None] = None

    def play(self, board):
        self.played = True
        print("Played Year of Plenty")
        # TODO: Take any two resources from the bank

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value
