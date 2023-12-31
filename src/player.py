import random
from dataclasses import dataclass, field

from src.cards import Cards
from src.resources import Resources


@dataclass
class Player:
    name: str = ""
    color: str = ""
    score: int = 0
    type: str = "Bot"
    resources: Resources = field(default_factory=Resources)
    cards: Cards = field(default_factory=Cards)

    def roll(self):
        roll = random.randint(1, 6) + random.randint(1, 6)
        print(f"Roll: {roll}")
        if roll == 7:
            print("Robber!")
        return roll

    def collect(self):
        return random.randint(1, 6) + random.randint(1, 6)

    def build(self):
        self.building = False
        while not self.building:
            choice = input("1=settlement, 2=city, 3=road, 4=End: ")
            if choice == "1":
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
                    print(
                        f"{self.color} just built a Settlement. Score: {self.score}, Resources: {self.resources.resources}"
                    )
                else:
                    print("Not enough resources, please choose again")
                    self.build()
            elif choice == "2":
                if self.resources["wheat"] >= 2 and self.resources["ore"] >= 3:
                    self.resources["wheat"] -= 2
                    self.resources["ore"] -= 3
                    self.score += 1
                    print(
                        f"{self.color} just built a City. Score: {self.score}, Resources: {self.resources.resources}"
                    )
                else:
                    print("Not enough resources, please choose again")
                    self.build()
            elif choice == "3":
                if self.resources["brick"] >= 1 and self.resources["wood"] >= 1:
                    self.resources["brick"] -= 1
                    self.resources["wood"] -= 1
                    print(
                        f"{self.color} just built a Road. Score: {self.score}, Resources: {self.resources.resources}"
                    )
                else:
                    print("Not enough resources, please choose again")
                    self.build()
            elif choice == "4":
                self.building = True

    def trade(self):
        print("Trade")
