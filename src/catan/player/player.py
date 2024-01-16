from __future__ import annotations

import collections
import random
from dataclasses import dataclass, field
from typing import Dict, List

from src.catan.board.board import Board
from src.catan.buildings.buildings import Buildings, City, Road, Settlement
from src.catan.deck.cards import (
    Knight,
    Monopoly,
    RoadBuilding,
    VictoryPoint,
    YearOfPlenty,
)
from src.catan.deck.deck import CardDeck
from src.catan.game.auto_setup import setup
from src.catan.resources.resources import Resources


@dataclass
class Player:
    """
    Represents a player in the game of Catan.

    Attributes:
        name (None | int): The name or identifier of the player.
        color (None | str): The color associated with the player.
        score (int): The current score of the player.
        type (None | str): The type or role of the player.
        buildings (Buildings): The buildings owned by the player.
        resources (Resources): The resources owned by the player.
        cards (List[Knight | VictoryPoint | Monopoly | RoadBuilding | YearOfPlenty]): The development cards owned by the player.
        longest_road (bool): Indicates if the player has the longest road.
        largest_army (bool): Indicates if the player has the largest army.
    """

    name: None | int = None
    color: None | str = None
    score: int = 0
    type: None | str = None
    buildings: Buildings = field(default_factory=Buildings)
    resources: Resources = field(default_factory=Resources)
    cards: List[Knight | VictoryPoint | Monopoly | RoadBuilding | YearOfPlenty] = field(
        default_factory=list
    )
    longest_road: bool = False
    largest_army: bool = False

    def roll(self) -> int:
        """
        Simulates rolling two dice and returns the sum of the two dice.

        Returns:
            int: The sum of the two dice rolls.
        """
        roll = random.randint(1, 6) + random.randint(1, 6)
        print(f"Roll: {roll}")
        return roll

    def build(
        self, board: Board, players: List[Player], setup: bool = False, auto=False
    ) -> None:
        """
        Builds settlements, cities, and roads for the player.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.
            setup (bool, optional): Indicates if it is the setup phase. Defaults to False.
            auto (bool, optional): Indicates if the building process is automated. Defaults to False.

        Returns:
            None
        """
        self.end_building = False
        while not self.end_building:
            if setup and auto:
                self.build_settlement(board, players, auto=True)
                self.build_road(board, players, auto=True)
                self.end_building = True

            if setup and not auto:
                self.build_settlement(board, players)
                board.display()
                self.build_road(board, players)
                board.display()
                self.end_building = True

            if not setup:
                choice = int(input("1=Settlement, 2=City, 3=Road, 4=End: "))
                if choice == 1:
                    self.build_settlement(board, players)
                elif choice == 2:
                    self.build_city(board, players)
                elif choice == 3:
                    self.build_road(board, players)
                elif choice == 4:
                    self.end_building = True

    def build_settlement(
        self, board: Board, players: List[Player], auto: bool = False
    ) -> None:
        """
        Builds a settlement on the game board.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players.
            auto (bool, optional): Flag indicating if the settlement should be built automatically. Defaults to False.
        """
        if auto:
            node_id = setup[self.name][0]["settlement"]
            if board.nodes[node_id].occupied:
                node_id = setup[self.name][1]["settlement"]

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

        elif (
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
                self.build_settlement(board, players)

        else:
            print("Not enough resources to build a settlement, please choose again")
            self.build(board, players)

    def build_city(self, board: Board, players: List[Player]) -> None:
        """
        Builds a city on the game board if the player has enough resources.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            None
        """
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
                self.build_city(board, players)
        else:
            print("Not enough resources to build a city, please choose again")
            self.build(board, players)

    def replace_settlement(self, node_id: int) -> None:
        """
        Removes a settlement from the player's buildings based on the given node ID.

        Args:
            node_id (int): The ID of the node representing the settlement to be removed.

        Returns:
            None
        """
        for settlement in self.buildings.settlements:
            if settlement.id == node_id:
                self.buildings.settlements.remove(settlement)
                self.score -= 1

    def build_road(
        self,
        board: Board,
        players: List[Player],
        dev_card: bool = False,
        auto: bool = False,
    ) -> None:
        """
        Builds a road for the player.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.
            dev_card (bool, optional): Indicates if the road is being built using a development card. Defaults to False.
            auto (bool, optional): Indicates if the road should be automatically built. Defaults to False.
        """
        if auto:
            self.auto_build_road(board)

        elif self.resources.brick.count >= 1 and self.resources.wood.count >= 1:
            self.build_road_default(board, players)
        elif dev_card:
            self.build_road_dev_card(board)
        else:
            print("Not enough resources to build a road, please choose again")
            self.build(board, players)

        player_road_lengths = self.check_longest_road(board, players)
        self.assign_longest_road(player_road_lengths, players)

    def assign_longest_road(
        self, player_road_lengths: Dict[Player, int], players: List[Player]
    ) -> None:
        """
        Assigns the longest road to the current player based on the road lengths of all players.

        Args:
            player_road_lengths (Dict[Player, int]): A dictionary mapping players to their road lengths.
            players (List[Player]): A list of all players in the game.

        Returns:
            None
        """
        lr_player = [player for player in players if player.longest_road]
        lr_length = player_road_lengths[lr_player[0]] if len(lr_player) > 0 else 0

        if len(lr_player) == 0 and player_road_lengths[self] >= 5:
            self.longest_road = True
            self.score += 2
            print(f"{self.color} acquired the longest road.")
        elif player_road_lengths[self] > lr_length and player_road_lengths[self] >= 5:
            self.longest_road = True
            self.score += 2
            lr_player[0].longest_road = False
            lr_player[0].score -= 2
            print(f"{self.color} acquired the longest road from {lr_player[0].color}.")
        else:
            pass

    def check_longest_road(
        self, board: Board, players: List[Player]
    ) -> Dict[Player, int]:
        """
        Calculates the length of the longest road for each player on the board.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            Dict[Player, int]: A dictionary mapping each player to their longest road length.
        """
        player_lengths = dict()
        for player in players:
            player_roads = player.buildings.roads
            current_road_ids = [road.id for road in player_roads]
            mapping = list()
            for edge_id in current_road_ids:
                edge = board.edges[edge_id]
                for adj_edge in edge.edges:
                    joining_node = board._node(
                        list(set(edge.nodes) & set(board._edge(adj_edge).nodes))[0]
                    )
                    if (
                        edge.color == player.color
                        and board.edges[adj_edge].color == player.color
                        and (joining_node.color in [player.color, None])
                    ):
                        mapping.append((edge_id, adj_edge))

            # TODO: improve this to handle multiple paths
            if len(mapping) != 0:
                graph = self.build_adjacency_list(mapping)
                visited = set()
                vertex = [key for key in graph.keys()][0]
                player_lengths[player] = self.dfs(graph, vertex, visited) + 1
            else:
                player_lengths[player] = 0

        return player_lengths

    def dfs(self, graph: dict, vertex: int, visited: set, depth=0) -> int:
        """
        Performs a depth-first search (DFS) on a graph starting from a given vertex.

        Args:
            graph (dict): The graph represented as an adjacency list.
            vertex (int): The starting vertex for the DFS.
            visited (set): A set to keep track of visited vertices.
            depth (int, optional): The current depth of the DFS. Defaults to 0.

        Returns:
            int: The maximum depth reached during the DFS traversal.
        """
        visited.add(vertex)
        max_depth = depth  # Initialize max_depth for the current node

        for neighbor in graph[vertex]:
            if neighbor not in visited:
                max_depth = max(
                    max_depth, self.dfs(graph, neighbor, visited, depth + 1)
                )

        return max_depth

    def build_adjacency_list(self, edges: list) -> Dict[int, List[int]]:
        """
        Builds an adjacency list from a list of edges.

        Args:
            edges (list): A list of edges represented as tuples.

        Returns:
            dict: An adjacency list where the keys are the source vertices and the values are lists of destination vertices.

        Example:
            >>> edges = [(1, 2), (2, 3), (1, 3)]
            >>> build_adjacency_list(edges)
            {1: [2, 3], 2: [1, 3], 3: [1, 2]}
        """
        adjacency_list: dict = {}
        for edge in edges:
            source, destination = edge
            if source not in adjacency_list:
                adjacency_list[source] = []
            adjacency_list[source].append(destination)

        for key in adjacency_list.keys():
            adjacency_list[key] = list(set(adjacency_list[key]))

        adjacency_list = collections.OrderedDict(sorted(adjacency_list.items()))
        return adjacency_list

    def auto_build_road(self, board: Board) -> None:
        """
        Automatically builds a road for the player on the given board.

        Args:
            board (Board): The game board on which the road is built.

        Returns:
            None
        """
        edge_id = setup[self.name][0]["road"]
        if board.edges[edge_id].occupied:
            edge_id = setup[self.name][1]["road"]

        road = Road(self.color, edge_id)
        self.resources.brick.count -= 1
        self.resources.wood.count -= 1

        self.buildings.roads.append(road)
        board.edges[edge_id].occupied = True
        board.edges[edge_id].color = self.color

    def build_road_default(self, board: Board, players: List[Player]) -> None:
        """
        Builds a road for the player using the default strategy.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            None
        """
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
            self.build_road(board, players)

    def build_road_dev_card(self, board: Board, players: List[Player]) -> None:
        """
        Builds a road using a development card.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            None
        """
        edge_id = int(input("Choose road location - [0-71]:"))
        nearby_edge_ids = board.edges[edge_id].edges
        nearby_node_ids = board.edges[edge_id].nodes
        nearby_edge_colors = [board.edges[edge].color for edge in nearby_edge_ids]
        nearby_nodes_colors = [board.nodes[node].color for node in nearby_node_ids]
        if board.edges[edge_id].occupied is False and self.color in (
            nearby_edge_colors + nearby_nodes_colors
        ):
            road = Road(self.color, edge_id)
            self.buildings.roads.append(road)
            board.edges[edge_id].occupied = True
            board.edges[edge_id].color = self.color
        else:
            print("Invalid location, select a build option again.")
            self.build_road(board, players, dev_card=True)

    def trade(self, board: Board, players: List[Player]) -> None:
        """
        Perform a trade action.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            None
        """
        rates = self.determine_trade_rates(board)
        trade_type = int(input("Player Trade (1), Bank/Port Trade (2), Cancel (3): "))

        if trade_type == 1:
            self.player_trade(players)
        elif trade_type == 2:
            self.bank_port_trade(rates, board, players)
        elif trade_type == 3:
            pass

    def bank_port_trade(
        self, rates: Dict[str, int], board: Board, players: List[Player]
    ) -> None:
        """
        Perform a bank/port trade with the specified rates.

        Args:
            rates (Dict[str, int]): A dictionary specifying the trade rates for each resource.
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            None
        """
        resource = input("Which resource would you like to trade: ")
        receive = input("Which resource would you like to receive: ")

        if self.resources[resource].count >= rates[resource]:
            self.resources[resource].count -= rates[resource]
            self.resources[receive].count += 1
            print(f"Traded {rates[resource]} {resource} for 1 {receive}")
        else:
            print("Not enough resources to trade, please choose again")
            self.trade(board, players)

    def player_trade(self, players: List[Player]) -> None:
        """
        Allows the player to initiate a trade with other players.

        Args:
            players (List[Player]): A list of Player objects representing the other players in the game.

        Returns:
            None
        """
        print(f"{self.color} has {self.resources}")
        resource = input("Which resource would you like to trade: ")
        get_amount = int(input("How many would you like to trade: "))
        receive = input("Which resource would you like to receive: ")
        receive_amount = int(input("How many would you like to trade: "))

        traded = False
        while not traded:
            for player in players:
                if (
                    player.color != self.color
                    and player.resources[resource].count >= receive_amount
                ):
                    player_accept = input(
                        f"{player.color} would you like to trade {resource} for {receive} [Y/N]: "
                    ).upper()
                    if player_accept == "Y":
                        player.resources[resource].count -= receive_amount
                        player.resources[receive].count += get_amount
                        self.resources[resource].count += receive_amount
                        self.resources[receive].count -= get_amount
                        print(f"Traded {resource} for {receive}")
                        traded = True
                    elif player_accept == "N":
                        print(f"{player.color} declined trade.")
                else:
                    print("Player does not have enough resources to trade.")
        print(f"{self.color} has {self.resources}")

    def determine_trade_rates(self, board: Board) -> Dict[str, int]:
        """
        Determines the trade rates for the player based on their buildings and harbors.

        Args:
            board (Board): The game board.

        Returns:
            Dict[str, int]: A dictionary containing the trade rates for each resource.
                The keys are the resource names ("brick", "wood", "sheep", "wheat", "ore"),
                and the values are the corresponding trade rates.
        """
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

    def dev_card(self, board: Board, players: List[Player], deck: CardDeck) -> None:
        """
        Allows the player to interact with development cards.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.
            deck (CardDeck): The deck of development cards.
        """
        self._dev_card = False
        while not self._dev_card:
            choice = input("1=Collect, 2=Play, 3=End:")
            if choice == "1":
                self.collect_dev_card(board, deck)
            elif choice == "2":
                self.select_dev_card_to_play(board, players)
            elif choice == "3":
                self._dev_card = True

    def collect_dev_card(self, deck: CardDeck) -> None:
        """
        Collects a development card from the given deck if the player has enough resources.

        Args:
            deck (CardDeck): The deck of development cards.

        Returns:
            None
        """
        if (
            self.resources.sheep.count >= 1
            and self.resources.wheat.count >= 1
            and self.resources.ore.count >= 1
        ):
            self.resources.sheep.count -= 1
            self.resources.wheat.count -= 1
            self.resources.ore.count -= 1

            card = deck.select_dev_card()
            self.cards.append(card)
            print(f"Player {self.color} collected a {card.__class__.__name__} card.")

    def select_dev_card_to_play(self, board: Board, players: List[Player]) -> None:
        """
        Allows the player to select a development card to play.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            None
        """
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
                            self.play_dev_card(card, board, players)

    def play_dev_card(
        self,
        card: Knight | VictoryPoint | Monopoly | RoadBuilding | YearOfPlenty,
        board: Board,
        players: List[Player],
    ) -> None:
        """
        Plays a development card.

        Args:
            card (Knight | VictoryPoint | Monopoly | RoadBuilding | YearOfPlenty): The development card to be played.
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            None
        """
        if isinstance(card, Knight):
            self.play_kinght(card, board, players)
        elif isinstance(card, VictoryPoint):
            self.play_victory_point(card, board)
        elif isinstance(card, Monopoly):
            self.play_monopoly(card, board, players)
        elif isinstance(card, RoadBuilding):
            self.play_road_building(card, board, players)
        elif isinstance(card, YearOfPlenty):
            self.play_year_of_plenty(card, board)

        self.cards.remove(card)
        self._dev_card = True

        return None

    def play_kinght(self, board: Board, players: List[Player]) -> None:
        """
        Activates the knight and checks if the player has the largest army.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            None
        """
        self.activate_knight(board, players)
        self.check_largest_army(players)

    def activate_knight(self, board: Board, players: List[Player]) -> None:
        """
        Activates a knight card for the player.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            None
        """
        print("Played Knight")
        # move and update the robbber location
        robber_tile = board.get_robber_tile()

        robber_moved = False
        while not robber_moved:
            move_robber = int(input("Choosen a Tile [0-18] to move the Robber to: "))
            if move_robber == robber_tile.id:
                print("Robber must be moved to a different tile.")
            else:
                new_robber_tile = board.set_robber_tile(move_robber)
                new_robber_tile.robber = True
                robber_tile.robber = False
                robber_moved = True

        # choosen a player to steal a random resource from
        # if the player has no resources, they are skipped
        adjacent_nodes = new_robber_tile.get_near_nodes()

        able_to_steal_from = set()
        for node in adjacent_nodes:
            if isinstance(board.nodes[node].building, (Settlement, City)):
                able_to_steal_from.add(board.nodes[node].building.color)

        if self.color in able_to_steal_from:
            able_to_steal_from.remove(self.color)

        if len(able_to_steal_from) == 0:
            print("No players to steal from.")

        else:
            select_player = input(
                f"Choosen a player to steal from {able_to_steal_from}: "
            )

            robbed_player = [
                player
                for player in players
                if player.color in select_player and player.total_resources() > 0
            ]
            if len(robbed_player) == 0:
                print("No players to steal from.")
            else:
                robbed_player = robbed_player[0]
                available_resources = [
                    str(res.__class__.__name__).lower()
                    for key, res in robbed_player.resources.__dict__.items()
                    if res.count > 0
                ]
                random_resource = random.choice(list(available_resources))

                robbed_player.resources[random_resource].count -= 1
                self.resources[random_resource].count += 1
                print(
                    f"{self.color} stole {random_resource} from {robbed_player.color}."
                )

    def check_largest_army(self, players: List[Player]) -> None:
        """
        Checks if the current player has the largest army in the game and updates the scores accordingly.

        Args:
            players (List[Player]): A list of Player objects representing all the players in the game.

        Returns:
            None
        """
        la_active = any([player.largest_army for player in players])
        played_knights = len(
            [card for card in self.cards if isinstance(card, Knight) and card.played]
        )
        max_played = 0
        for player in players:
            knights_played = len(
                [
                    card
                    for card in player.cards
                    if isinstance(card, Knight) and card.played
                ]
            )
            if knights_played > max_played:
                max_played = knights_played

        if not la_active and played_knights >= 3:
            self.largest_army = True
            self.score += 2

        elif la_active and played_knights > max_played:
            active_la_player = [player for player in players if player.largest_army][0]
            self.largest_army = True
            self.score += 2
            active_la_player.largest_army = False
            active_la_player.score -= 2

    def play_victory_point(self) -> None:
        """
        Increases the player's score by 1 and prints a message indicating that a Victory Point card was played.

        Returns:
            None
        """
        self.score += 1
        print(f"Player {self.color} played a Victory Point card.")

    def play_monopoly(self, players: List[Player]) -> None:
        """
        Monopolizes a specific resource from other players.

        Args:
            players (List[Player]): A list of Player objects representing the other players.

        Returns:
            None
        """
        resource = input("Which resource would you like to monopolize: ")
        for player in players:
            if player.color != self.color:
                self.resources[resource].count += player.resources[resource].count
                player.resources[resource].count = 0

    def play_road_building(self, board: Board, players: List[Player]) -> None:
        """
        Plays the Road Building development card.

        Args:
            board (Board): The game board.
            players (List[Player]): The list of players in the game.

        Returns:
            None
        """
        print("Played Road Building")
        self.build_road(board, players=players, dev_card=True)
        self.build_road(board, players=players, dev_card=True)

    def play_year_of_plenty(self) -> None:
        """
        Allows the player to collect two resources of their choice.

        This method prompts the player to input the names of two resources they would like to collect.
        The count of the chosen resources in the player's resources dictionary is then incremented by 1.

        Parameters:
            None

        Returns:
            None
        """
        resource = input("Which resource would you like to collect: ")
        self.resources[resource].count += 1
        resource = input("Which resource would you like to collect: ")
        self.resources[resource].count += 1

    def total_resources(self) -> int:
        """
        Calculate the total number of resources owned by the player.

        Returns:
            int: The total number of resources owned by the player.
        """
        total = 0
        for resource in self.resources.__dict__:
            total += self.resources[resource].count
        return total

    def discard_resources(self, total: int) -> None:
        """
        Discard resources from the player's inventory.

        Args:
            total (int): The total number of resources to be discarded.

        Returns:
            None
        """
        discard_amount = total // 2
        print(
            f"Player {self.color} has too many resources, must discard {discard_amount}"
        )

        while discard_amount > 0:
            print(f"Player {self.color} has {self.resources}")
            discard = input(
                "Which resource would you like to discard: brick, wood, sheep, wheat, ore: "
            )
            if discard not in self.resources.all_resources():
                print("Invalid resource, please choose again.")
            elif self.resources[discard].count > 0:
                self.resources[discard].count -= 1
                discard_amount -= 1
            else:
                print("You do not have any of that resource, please choose again.")

    def __hash__(self) -> int:
        """
        Calculate the hash value of the player object.

        Returns:
            int: The hash value of the player object.
        """
        return hash(str(self))
