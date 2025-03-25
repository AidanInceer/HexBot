from __future__ import annotations

from typing import Dict, List, Set

from src.catan.board.board import Board


class RoadManager:
    """Analyzes road networks to determine the longest roads for players."""
    
    def __init__(self):
        """Initialize the RoadManager."""
        pass
    
    def check_longest_road(self, board: Board, players: List) -> Dict:
        """
        Checks the longest road for each player.
        
        Args:
            board (Board): The game board.
            players (List): The list of players in the game.
            
        Returns:
            Dict: A dictionary mapping player indices to their longest road lengths.
        """
        player_road_lengths = {}
        
        for player in players:
            # Find all edges containing the player's roads
            player_edges = []
            for edge_id, edge in enumerate(board.edges):
                if edge.color == player.color:
                    player_edges.append(edge_id)
            
            # Calculate longest path using DFS
            max_length = 0
            for edge_id in player_edges:
                visited = set()
                length = self._dfs_longest_path(board, edge_id, player.color, visited)
                max_length = max(max_length, length)
            
            player_road_lengths[player.name] = max_length
        
        return player_road_lengths
    
    def _dfs_longest_path(self, board: Board, edge_id: int, player_color: str, visited: Set[int]) -> int:
        """
        Depth-first search to find the longest path from a starting edge.
        
        Args:
            board (Board): The game board.
            edge_id (int): The starting edge ID.
            player_color (str): The color of the player.
            visited (Set[int]): Set of visited edge IDs.
            
        Returns:
            int: The length of the longest path.
        """
        if edge_id in visited or board.edges[edge_id].color != player_color:
            return 0
        
        visited.add(edge_id)
        max_path = 1  # Current edge counts as 1
        
        # Get all connected edges
        for connected_edge in board.edges[edge_id].edges:
            if connected_edge not in visited and board.edges[connected_edge].color == player_color:
                # Try each connected edge and update max_path
                length = 1 + self._dfs_longest_path(board, connected_edge, player_color, visited.copy())
                max_path = max(max_path, length)
        
        return max_path
    
    def assign_longest_road(self, player_road_lengths: Dict, players: List) -> None:
        """
        Assigns the 'longest road' status to the player with the longest road.
        
        Args:
            player_road_lengths (Dict): A dictionary mapping player indices to their longest road lengths.
            players (List): The list of players in the game.
            
        Returns:
            None
        """
        # Find the player with the longest road (must be at least 5 roads)
        max_length = 0
        max_player = None
        
        for player_name, length in player_road_lengths.items():
            if length >= 5 and length > max_length:
                max_length = length
                # Find the player object by name
                for player in players:
                    if player.name == player_name:
                        max_player = player
                        break
        
        # Reset longest road status for all players
        for player in players:
            if player.longest_road:
                player.score -= 2
                player.longest_road = False
        
        # Assign longest road to the player with the longest road
        if max_player is not None:
            max_player.longest_road = True
            max_player.score += 2
