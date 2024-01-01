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
    resources: Resources = field(default_factory=Resources)
    cards: Cards = field(default_factory=Cards)

    def roll(self):
        roll = random.randint(1, 6) + random.randint(1, 6)
        print(f"Roll: {roll}")
        if roll == 7:
            print("Robber!")
        return roll

    def build(self, board: Board, setup=False):
        self.end_building = False
        while not self.end_building:
            if setup:
                self.settlement(board)
                self.road(board)
                self.end_building = True

            if not setup:
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
            self.resources.brick.count >= 1
            and self.resources.wood.count >= 1
            and self.resources.sheep.count >= 1
            and self.resources.wheat.count >= 1
        ):
            self.resources.brick.count -= 1
            self.resources.wood.count -= 1
            self.resources.sheep.count -= 1
            self.resources.wheat.count -= 1
            self.score += 1
            node = int(input("Where would you like to build a settlement? [1-54]:"))
            settlement = Settlement(self.color, node)
            self.buildings.settlements.append(settlement)
            board.nodes[node].occupied = True
            board.nodes[node].building = settlement
            for node in board.nodes[node].nodes:
                board.nodes[node].occupied = True

        else:
            print("Not enough resources, please choose again")
            self.build(board)

    def city(self, board: Board):
        if self.resources.wheat.count >= 2 and self.resources.ore.count >= 3:
            self.resources.wheat.count -= 2
            self.resources.ore.count -= 3
            self.score += 1
            node = int(input("Where would you like to build a city? [1-54]:"))
            # if board.nodes[node].occupied: return to build -
            self.buildings.cities.append(City(self.color, node))
            city = City(self.color, node)
            self.buildings.cities.append(city)
            board.nodes[node].occupied = True
            board.nodes[node].building = city
            for node in board.nodes[node].nodes:
                board.nodes[node].occupied = True
        else:
            print("Not enough resources, please choose again")
            self.build(board)

    def road(self, board: Board):
        if self.resources.brick.count >= 1 and self.resources.wood.count >= 1:
            self.resources.brick.count -= 1
            self.resources.wood.count -= 1

            edge = int(input("Where would you like to build a road? [1-72]:"))
            self.buildings.roads.append(Road(self.color, edge))
        else:
            print("Not enough resources, please choose again")
            self.build(board)

    def trade(self):
        print("Trade")
