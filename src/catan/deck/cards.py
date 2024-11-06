from dataclasses import dataclass


@dataclass
class Knight:
    color: str | None = None
    played: bool = False
    player: str | None = None

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class VictoryPoint:
    color: str | None = None
    played: bool = False
    player: str | None = None

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class Monopoly:
    color: str | None = None
    played: bool = False
    player: str | None = None

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class RoadBuilding:
    color: str | None = None
    played: bool = False
    player: str | None = None

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value


@dataclass
class YearOfPlenty:
    color: str | None = None
    played: bool = False
    player: str | None = None

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self[key] = value
