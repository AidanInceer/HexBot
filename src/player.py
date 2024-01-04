import random
from dataclasses import dataclass, field
from typing import List, Union

from src.board.board import Board
from src.build.buildings import Buildings, City, Road, Settlement
from src.cards import Knight, Monopoly, RoadBuilding, VictoryPoint, YearOfPlenty
from src.resources import Resources


@dataclass
class Player:
    name: Union[None, str] = None
    color: Union[None, str] = None
    score: int = 0
    type: Union[None, str] = None
    buildings: Buildings = field(default_factory=Buildings)
    resources: Resources = field(default_factory=Resources)
    cards: List[
        Union[Knight, VictoryPoint, Monopoly, RoadBuilding, YearOfPlenty]
    ] = field(default_factory=list)

    def roll(self):
        roll = random.randint(1, 6) + random.randint(1, 6)
        print(f"Roll: {roll}")
        return roll

    def build(self, board: Board, setup=False):
        self.end_building = False
        while not self.end_building:
            if setup:
                self.build_settlement(board)
                self.build_road(board)
                self.end_building = True

            if not setup:
                choice = input("1=Settlement, 2=City, 3=Road, 4=End: ")
                if choice == "1":
                    self.build_settlement(board)
                elif choice == "2":
                    self.build_city(board)
                elif choice == "3":
                    self.build_road(board)
                elif choice == "4":
                    self.end_building = True

    def build_settlement(self, board: Board):
        # only build settlement if you have 1 brick, 1 wood, 1 sheep, 1 wheat.
        if (
            self.resources.brick.count >= 1
            and self.resources.wood.count >= 1
            and self.resources.sheep.count >= 1
            and self.resources.wheat.count >= 1
        ):
            node_id = int(input("Choose settlement location - [0-53]:"))

            # only build settlement if the node is not occupied and nearby nodes are not occupied.
            nearby_node_ids = board.nodes[node_id].nodes
            nearby_nodes = [board.nodes[node].occupied for node in nearby_node_ids]
            if board.nodes[node_id].occupied is False and all(nearby_nodes) is False:
                # update the board to show the settlement, set nearby nodes to occupied
                settlement = Settlement(self.color, node_id)
                self.resources.brick.count -= 1
                self.resources.wood.count -= 1
                self.resources.sheep.count -= 1
                self.resources.wheat.count -= 1
                self.score += 1
                self.buildings.settlements.append(settlement)
                board.nodes[node_id].occupied = True
                board.nodes[node_id].building = settlement
                board.nodes[node_id].color = self.color
                for node in board.nodes[node_id].nodes:
                    board.nodes[node].occupied = True
            else:
                print("Invalid location, select a build option again.")
                self.build_settlement(board)

        else:
            print("Not enough resources to build a settlement, please choose again")
            self.build(board)

    def build_city(self, board: Board):
        # Only build city if you have 2 wheat and 3 ore.
        if self.resources.wheat.count >= 2 and self.resources.ore.count >= 3:
            # Get the node id of the city.
            node_id = int(input("Choose city location - [0-53]:"))

            # Check if there is a settlement at the node.
            if (
                board.nodes[node_id].occupied
                and board.nodes[node_id].building == "settlement"
            ):
                # Remove the settlement and replace it with a city at the same node.
                self.replace_settlement(node_id=node_id)

                # Update the board to show the city, set nearby nodes to occupied
                city = City(self.color, node_id)
                self.resources.wheat.count -= 2
                self.resources.ore.count -= 3
                self.score += 2
                self.buildings.cities.append(city)
                board.nodes[node_id].building = city
                board.nodes[node_id].occupied = True
                board.nodes[node_id].color = self.color
                for node in board.nodes[node_id].nodes:
                    board.nodes[node].occupied = True
            else:
                print("Invalid location, select a build option again.")
                self.build_city(board)
        else:
            print("Not enough resources to build a city, please choose again")
            self.build(board)

    def replace_settlement(self, node_id: int):
        for settlement in self.buildings.settlements:
            if settlement.id == node_id:
                self.buildings.settlements.remove(settlement)
                self.score -= 1
                return

    def build_road(self, board: Board):
        if self.resources.brick.count >= 1 and self.resources.wood.count >= 1:
            edge_id = int(input("Choose road location - [0-71]:"))
            nearby_edge_ids = board.edges[edge_id].edges
            nearby_node_ids = board.edges[edge_id].nodes
            nearby_edge_colors = [board.edges[edge].color for edge in nearby_edge_ids]
            nearby_nodes_colors = [board.nodes[node].color for node in nearby_node_ids]
            if board.edges[edge_id].occupied is False and self.color in (
                nearby_edge_colors + nearby_nodes_colors
            ):
                road = Road(self.color, edge_id)
                self.resources.brick.count -= 1
                self.resources.wood.count -= 1

                self.buildings.roads.append(road)
                board.edges[edge_id].occupied = True
                board.edges[edge_id].color = self.color
            else:
                print("Invalid location, select a build option again.")
                self.build_road(board)
        else:
            print("Not enough resources to build a road, please choose again")
            self.build_road(board)

    def trade(self, board: Board):
        rates = self.determine_trade_rates(board)
        # Trade with bank
        # select a resource to trade
        trade_type = int(input("Player Trade (1), Bank/Port Trade (2), Cancel (3): "))
        if trade_type == 2:
            resource = input("Which resource would you like to trade: ")
            receive = input("Which resource would you like to receive: ")

            if self.resources[resource].count >= rates[resource]:
                self.resources[resource].count -= rates[resource]
                self.resources[receive].count += 1

                print(f"Traded {rates[resource]} {resource} for 1 {receive}")
            else:
                print("Not enough resources to trade, please choose again")
                self.trade(board)

        elif trade_type == 3:
            pass

    def determine_trade_rates(self, board: Board):
        base_rates = {
            "brick": 4,
            "wood": 4,
            "sheep": 4,
            "wheat": 4,
            "ore": 4,
        }

        # Get players nodes with buildings.
        players_buildings = self.buildings.settlements + self.buildings.cities
        player_building_ids = [building.id for building in players_buildings]
        player_nodes = []
        for id in player_building_ids:
            node = board.nodes[id]
            player_nodes.append(node)

        harbor_rates = {}
        for node in player_nodes:
            if len(node.harbors) > 0:
                for harbor_id in node.harbors:
                    harbor = board.harbors[harbor_id]
                    if harbor.resource == "all":
                        harbor_rates = {
                            "brick": 3,
                            "wood": 3,
                            "sheep": 3,
                            "wheat": 3,
                            "ore": 3,
                        }
                for harbor_id in node.harbors:
                    harbor = board.harbors[harbor_id]
                    harbor_rates[harbor.resource] = harbor.rate

        return {**base_rates, **harbor_rates}

    def dev_card(self, board: Board):
        self._dev_card = False
        while not self._dev_card:
            choice = input("1=Collect, 2=Play, 3=End:")
            if choice == "1":
                self.collect_dev_card(board)
            elif choice == "2":
                self.select_dev_card_to_play(board)
            elif choice == "3":
                self._dev_card = True

    def collect_dev_card(self, board: Board):
        if (
            self.resources.sheep.count >= 1
            and self.resources.wheat.count >= 1
            and self.resources.ore.count >= 1
        ):
            self.resources.sheep.count -= 1
            self.resources.wheat.count -= 1
            self.resources.ore.count -= 1
            selected = board.select_dev_card()
            if selected is not None:
                self.cards.append(selected)
                self._dev_card = False
                print(f"Collected Development Card: {selected.__class__.__name__}")
            else:
                print("No more dev cards left")

    def select_dev_card_to_play(self, board: Board):
        if len(self.cards) > 0:
            chosen = input("Which dev card would you like to play: ")
            card_types = [
                ("knight", Knight),
                ("victory_point", VictoryPoint),
                ("monopoly", Monopoly),
                ("road_building", RoadBuilding),
                ("year_of_plenty", YearOfPlenty),
            ]
            for card_type in card_types:
                if chosen == card_type[0]:
                    for card in self.cards:
                        if isinstance(card, card_type[1]):
                            self.play_dev_card(card, board)

    def play_dev_card(
        self,
        card: Union[Knight, VictoryPoint, Monopoly, RoadBuilding, YearOfPlenty],
        board: Board,
    ):
        card.play(board)
        self.cards.remove(card)
        self.dev_card = True

    def total_resources(self) -> int:
        total = 0
        for resource in self.resources.__dict__:
            total += self.resources[resource].count
        return total

    def discard_resources(self, total: int):
        discard_amount = total // 2
        print(
            f"Player {self.color} has too many resources, must discard {discard_amount}"
        )

        while discard_amount > 0:
            print(f"Player {self.color} has {self.resources}")
            discard = input(
                "Which resource would you like to discard: brick, wood, sheep, wheat, ore: "
            )
            if discard not in self.resources:
                print("Invalid resource, please choose again.")
            elif self.resources[discard].count > 0:
                self.resources[discard].count -= 1
                discard_amount -= 1
            else:
                print("You do not have any of that resource, please choose again.")
