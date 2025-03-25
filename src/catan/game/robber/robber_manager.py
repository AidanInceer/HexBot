import random

from src.catan.board.tile import Tile
from src.catan.buildings.buildings import City, Settlement
from src.catan.player.player import Player
from src.catan.resources.resources import Brick, Ore, Sheep, Wheat, Wood
from src.interface.input_handler import InputHandler
TYPES = (
    Brick,
    Ore,
    Sheep,
    Wheat,
    Wood,
)


class RobberManager:
    """
    Manages all robber-related functionality in the Catan game.
    """

    def __init__(self, board, players):
        """
        Initialize the RobberManager with the game board and players.

        Args:
            board: The game board
            players: List of players in the game
        """
        self.board = board
        self.players = players

    def activate_robber(self, current_player: Player) -> None:
        """
        Activates the robber and allows the current player to move it to a different tile.
        If there are adjacent players with resources, the current player can steal a random resource from one of them.
        If any player has more than 7 cards, they must discard half of their resources.

        Parameters:
            current_player (Player): The current player who activated the robber.

        Returns:
            None
        """
        # move the robber to a different tile
        new_robber_tile = self.move_robber_tile(current_player)

        # choose a player to steal a random resource from
        # if the player has no resources, they are skipped
        able_to_steal_from = self.determine_who_to_steal_from(
            current_player, new_robber_tile
        )

        if able_to_steal_from:
            robbed_player = self.select_player_to_steal_from(able_to_steal_from,current_player)
            if robbed_player:
                self.steal_random_resource(robbed_player, current_player)

        # if any player has more than 7 cards, they must discard half
        self.robber_discard_resources()

    def move_robber_tile(self, current_player: Player) -> Tile:
        """
        Moves the robber to a different tile selected by the player.

        Returns:
            Tile: The new tile where the robber is placed
        """
        robber_tile = self.board.get_robber_tile()
        robber_moved = False
        while not robber_moved:
            choice = InputHandler(
                value_range=range(0, 18, 1),
                user=current_player.type,
                input_type="int",
                message="Choosen a Tile [0-18] to move the Robber to: ",
            ).process()
            if choice < 0 or choice > 18:
                print("Invalid tile.")
            elif choice == robber_tile.id:
                print("Robber must be moved to a different tile.")
            else:
                new_robber_tile = self.board.set_robber_tile(choice)
                new_robber_tile.robber = True
                robber_tile.robber = False
                robber_moved = True

        return new_robber_tile

    def select_player_to_steal_from(self, able_to_steal_from: set, current_player: Player) -> Player:
        """
        Allows the current player to select another player to steal from.

        Args:
            able_to_steal_from (set): Set of player colors that can be stolen from

        Returns:
            Player: The selected player to steal from, or None if no valid player
        """
        select_player = InputHandler(
            value_range=able_to_steal_from,
            user=current_player.type,
            input_type="player",
            message=f"Choose a player to steal from {able_to_steal_from}: ",
        ).process()

        robbed_player = [
            player
            for player in self.players
            if player.color in select_player and player.total_resources() > 0
        ]
        if len(robbed_player) == 0:
            print("No players to steal from.")

        return robbed_player

    def steal_random_resource(
        self, robbed_player: Player, current_player: Player
    ) -> None:
        """
        Steals a random resource from the robbed player and gives it to the current player.

        Args:
            robbed_player (Player): The player being robbed
            current_player (Player): The player doing the robbing

        Returns:
            None
        """
        robbed_player = robbed_player[0]

        # Get the available resources of the robbed player
        available_resources = [
            resource_name.lower()
            for resource_name, resource in robbed_player.resources.__dict__.items()
            if isinstance(resource, TYPES) and resource.count > 0
        ]

        # Choose a random resource to steal
        random_resource = random.choice(list(available_resources))

        # Update the resource counts for the current player and the robbed player
        robbed_player.resources[random_resource].count -= 1
        current_player.resources[random_resource].count += 1

        print(
            f"{current_player.color} stole {random_resource} from {robbed_player.color}."
        )

    def determine_who_to_steal_from(
        self, current_player: Player, new_robber_tile: Tile
    ) -> set:
        """
        Determines which players can be stolen from based on the new robber tile location.

        Args:
            current_player (Player): The current player
            new_robber_tile (Tile): The tile where the robber was placed

        Returns:
            set: Set of player colors that can be stolen from
        """
        adjacent_nodes = new_robber_tile.get_near_nodes()

        able_to_steal_from = set()
        for node in adjacent_nodes:
            if isinstance(self.board.nodes[node].building, (Settlement, City)):
                able_to_steal_from.add(self.board.nodes[node].building.color)

        if current_player.color in able_to_steal_from:
            able_to_steal_from.remove(current_player.color)

        if len(able_to_steal_from) == 0:
            print("No players to steal from.")

        return able_to_steal_from

    def robber_discard_resources(self) -> None:
        """
        Forces players with more than 7 resources to discard half of their resources.

        Returns:
            None
        """
        for player in self.players:
            total = player.total_resources()
            if total > 7:
                player.discard_resources(total)
