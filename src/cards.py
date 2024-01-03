from dataclasses import dataclass
from typing import Union


@dataclass
class Knight:
    color: Union[str, None] = None
    played: bool = False
    player: Union[str, None] = None

    def play(self):
        self.played = True
        print("Played Knight")

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class VictoryPoint:
    color: Union[str, None] = None
    played: bool = False
    player: Union[str, None] = None

    def play(self):
        self.played = True
        print("Played Victory Point")

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class Monopoly:
    color: Union[str, None] = None
    played: bool = False
    player: Union[str, None] = None

    def play(self):
        self.played = True
        print("Played Monopoly")

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class RoadBuilding:
    color: Union[str, None] = None
    played: bool = False
    player: Union[str, None] = None

    def play(self):
        self.played = True
        print("Played Road Building")

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class YearOfPlenty:
    color: Union[str, None] = None
    played: bool = False
    player: Union[str, None] = None

    def play(self):
        self.played = True
        print("Played Year of Plenty")

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value
