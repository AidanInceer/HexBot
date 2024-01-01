import random
from dataclasses import dataclass, field

from src.board.board import Board
from src.build.buildings import Buildings, City, Road, Settlement
from src.cards import Cards
from src.resources import Resources


@dataclass
class Player:
    name: str = ""
    color: str = ""
    score: int = 0
    type: str = "Bot"
    buildings: Buildings = field(default_factory=Buildings)
    dev_cards: list = field(default_factory=list)
    resources: Resources = field(default_factory=Resources)
    cards: Cards = field(default_factory=Cards)

    def roll(self):
        roll = random.randint(1, 6) + random.randint(1, 6)
        print(f"Roll: {roll}")
        if roll == 7:
            print("Robber!")
        return roll

    def build(self, board: Board):
        self.end_building = False
        while not self.end_building:
            choice = input("1=Settlement, 2=City, 3=Road, 4=End: ")
            if choice == "1":
                self.settlement(board)
            elif choice == "2":
                self.city(board)
            elif choice == "3":
                self.road(board)
            elif choice == "4":
                self.end_building = True

    def settlement(self, board: Board):
        if (
            self.resources["brick"] >= 1
            and self.resources["wood"] >= 1
            and self.resources["sheep"] >= 1
            and self.resources["wheat"] >= 1
        ):
            self.resources["brick"] -= 1
            self.resources["wood"] -= 1
            self.resources["sheep"] -= 1
            self.resources["wheat"] -= 1
            self.score += 1
            node = int(input("Where would you like to build? [1-54]:"))
            self.buildings.settlements.append(Settlement(self.color, node))

        else:
            print("Not enough resources, please choose again")
            self.build(board)

    def city(self, board: Board):
        if self.resources["wheat"] >= 2 and self.resources["ore"] >= 3:
            self.resources["wheat"] -= 2
            self.resources["ore"] -= 3
            self.score += 1
            node = int(input("Where would you like to build? [1-54]:"))
            self.buildings.cities.append(City(self.color, node))
        else:
            print("Not enough resources, please choose again")
            self.build(board)

    def road(self, board: Board):
        if self.resources["brick"] >= 1 and self.resources["wood"] >= 1:
            self.resources["brick"] -= 1
            self.resources["wood"] -= 1

            edge = int(input("Where would you like to build? [1-72]:"))
            self.buildings.roads.append(Road(self.color, edge))
        else:
            print("Not enough resources, please choose again")
            self.build(board)

    def trade(self):
        print("Trade")
