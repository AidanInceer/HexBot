from __future__ import annotations

from typing import List

from src.catan.board.board import Board
from src.catan.buildings.buildings import Buildings, City, Road, Settlement
from src.catan.game.setup.auto_setup import setup
from src.interface.input_handler import InputHandler


class BuildingManager:
    """Manages a player's building operations."""
    
    def __init__(self, player, buildings=None):
        self.player = player
        self.buildings = buildings or Buildings()
    
    def build_settlement(self, board: Board, players: List, auto: bool = False) -> None:
        """
        Builds a settlement on the game board.

        Args:
            board (Board): The game board.
            players (List): The list of players.
            auto (bool, optional): Flag indicating if the settlement should be built automatically. Defaults to False.
        """
        if auto:
            node_id = setup[self.player.name][0]["settlement"]
            if board.nodes[node_id].occupied:
                node_id = setup[self.player.name][1]["settlement"]

            settlement = Settlement(self.player.color, node_id)
            self.player.resource_manager.deduct_settlement_cost()
            self.player.score += 1
            self.buildings.settlements.append(settlement)
            board.nodes[node_id].occupied = True
            board.nodes[node_id].building = settlement
            board.nodes[node_id].color = self.player.color
            for node in board.nodes[node_id].nodes:
                board.nodes[node].occupied = True

        elif self.player.resource_manager.has_resources_for_settlement():
            available_nodes = board.fetch_best_available_node(building_type="settlement", player_color=self.player.color)
            if not available_nodes:
                print("No valid settlement locations available")
                return
                
            node_id = InputHandler(
                value_range=available_nodes,
                user=self.player.type,
                input_type="int",
                message="Choose settlement location from best options: ",
            ).process()

            # only build settlement if the node is not occupied and nearby nodes are not occupied.
            nearby_node_ids = board.nodes[node_id].nodes
            nearby_nodes = [board.nodes[node].occupied for node in nearby_node_ids]
            if board.nodes[node_id].occupied is False and all(nearby_nodes) is False:
                # update the board to show the settlement, set nearby nodes to occupied
                settlement = Settlement(self.player.color, node_id)
                self.player.resource_manager.deduct_settlement_cost()
                self.player.score += 1
                self.buildings.settlements.append(settlement)
                board.nodes[node_id].occupied = True
                board.nodes[node_id].building = settlement
                board.nodes[node_id].color = self.player.color
                for node in board.nodes[node_id].nodes:
                    board.nodes[node].occupied = True
            else:
                print("Building settlement failed, Invalid location")
                return
        else:
            print("Not enough resources to build a settlement")
            return

    def build_city(self, board: Board, players: List) -> None:
        """
        Builds a city on the game board if the player has enough resources.

        Args:
            board (Board): The game board.
            players (List): The list of players in the game.

        Returns:
            None
        """
        # Only build city if you have 2 wheat and 3 ore.
        if self.player.resource_manager.has_resources_for_city():
            # Get the node id of the city.
            available_nodes = board.fetch_best_available_node(building_type="city", player_color=self.player.color)
            if not available_nodes:
                print("No valid city locations available")
                return
                
            node_id = InputHandler(
                value_range=available_nodes,
                user=self.player.type,
                input_type="int",
                message="Choose city location from best options: ",
            ).process()

            # Check if there is a settlement at the node.
            if board.nodes[node_id].occupied and isinstance(
                board.nodes[node_id].building, Settlement
            ):
                # Remove the settlement and replace it with a city at the same node.
                self.replace_settlement(node_id=node_id)

                # Update the board to show the city, set nearby nodes to occupied
                city = City(self.player.color, node_id)
                self.player.resource_manager.deduct_city_cost()
                self.player.score += 2
                self.buildings.cities.append(city)
                board.nodes[node_id].building = city
                board.nodes[node_id].occupied = True
                board.nodes[node_id].color = self.player.color
                for node in board.nodes[node_id].nodes:
                    board.nodes[node].occupied = True
            else:
                print("Building city failed, Invalid location, select a build option again.")
                self.build_city(board, players)
        else:
            print("Not enough resources to build a city, please choose again")
            self.player.build(board, players)

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
                self.player.score -= 1

    def build_road(
        self,
        board: Board,
        players: List,
        road_manager,
        dev_card: bool = False,
        auto: bool = False,
    ) -> None:
        """
        Builds a road for the player.

        Args:
            board (Board): The game board.
            players (List): The list of players in the game.
            road_manager: The manager for road networks.
            dev_card (bool, optional): Indicates if the road is being built using a development card. Defaults to False.
            auto (bool, optional): Indicates if the road should be automatically built. Defaults to False.
        """
        if auto:
            self.auto_build_road(board)

        elif self.player.resource_manager.has_resources_for_road():
            self.build_road_default(board, players, road_manager)
        elif dev_card:
            self.build_road_dev_card(board, players, road_manager)
        else:
            print("Not enough resources to build a road, please choose again")
            self.player.build(board, players)

        player_road_lengths = road_manager.check_longest_road(board, players)
        road_manager.assign_longest_road(player_road_lengths, players)

    def auto_build_road(self, board: Board) -> None:
        """
        Automatically builds a road for the player on the given board.

        Args:
            board (Board): The game board on which the road is built.

        Returns:
            None
        """
        edge_id = setup[self.player.name][0]["road"]
        if board.edges[edge_id].occupied:
            edge_id = setup[self.player.name][1]["road"]

        road = Road(self.player.color, edge_id)
        self.player.resource_manager.deduct_road_cost()

        self.buildings.roads.append(road)
        board.edges[edge_id].occupied = True
        board.edges[edge_id].color = self.player.color

    def build_road_default(self, board: Board, players: List, road_manager) -> None:
        """
        Builds a road for the player using the default strategy.

        Args:
            board (Board): The game board.
            players (List): The list of players in the game.
            road_manager: The manager for road networks.

        Returns:
            None
        """
        available_edges = board.fetch_best_available_edge(self.player.color)
        if not available_edges:
            print("No valid road locations available.")
            return
    
        edge_id = InputHandler(
            value_range=available_edges,
            user=self.player.type,
            input_type="int",
            message="Choose road location - [0-71]: ",
        ).process()
        nearby_edge_ids = board.edges[edge_id].edges
        nearby_node_ids = board.edges[edge_id].nodes
        nearby_edge_colors = [board.edges[edge].color for edge in nearby_edge_ids]
        nearby_nodes_colors = [board.nodes[node].color for node in nearby_node_ids]
        if board.edges[edge_id].occupied is False and self.player.color in (
            nearby_edge_colors + nearby_nodes_colors
        ):
            road = Road(self.player.color, edge_id)
            self.player.resource_manager.deduct_road_cost()

            self.buildings.roads.append(road)
            board.edges[edge_id].occupied = True
            board.edges[edge_id].color = self.player.color
        else:
            print("Building road failed, Invalid location, select a build option again.")
            self.build_road(board, players, road_manager)

    def build_road_dev_card(self, board: Board, players: List, road_manager) -> None:
        """
        Builds a road using a development card.

        Args:
            board (Board): The game board.
            players (List): The list of players in the game.
            road_manager: The manager for road networks.

        Returns:
            None
        """
        available_edges = board.fetch_best_available_edge(self.player.color, dev_card=True)
        if not available_edges:
            print("No valid road locations available.")
            return
        
        edge_id = InputHandler(
            value_range=available_edges,
            user=self.player.type,
            input_type="int",
            message="Choose road location - [0-71]: ",
        ).process()
        nearby_edge_ids = board.edges[edge_id].edges
        nearby_node_ids = board.edges[edge_id].nodes
        nearby_edge_colors = [board.edges[edge].color for edge in nearby_edge_ids]
        nearby_nodes_colors = [board.nodes[node].color for node in nearby_node_ids]
        if board.edges[edge_id].occupied is False and self.player.color in (
            nearby_edge_colors + nearby_nodes_colors
        ):
            road = Road(self.player.color, edge_id)
            self.buildings.roads.append(road)
            board.edges[edge_id].occupied = True
            board.edges[edge_id].color = self.player.color
        else:
            print("Building road failed, Invalid location, select a build option again.")
            self.build_road(board, players, road_manager, dev_card=True)
