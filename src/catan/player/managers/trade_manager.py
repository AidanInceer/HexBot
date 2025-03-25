from __future__ import annotations

from typing import Dict, List

from src.catan.board.board import Board
from src.interface.input_handler import InputHandler


class TradeManager:
    """Manages trading operations for a player."""
    
    def __init__(self, player):
        self.player = player
    
    def trade(self, board: Board, players: List) -> None:
        """
        Perform a trade action.

        Args:
            board (Board): The game board.
            players (List): The list of players in the game.

        Returns:
            None
        """
        choice = InputHandler(
            value_range=[1, 2, 3],
            user=self.player.type,
            input_type="action",
            message="1=Player trade, 2=Bank trade, 3=End: ",
        ).process()
        if choice == 1:
            self.player_trade(players)
        elif choice == 2:
            self.bank_trade(board)
        elif choice == 3:
            pass
    
    def player_trade(self, players: List) -> None:
        """
        Perform a trade with another player.

        Args:
            players (List): The list of players in the game.

        Returns:
            None
        """
        # Select player to trade with
        player_ids = list(range(len(players)))
        player_ids.remove(self.player.name)
        choice = InputHandler(
            value_range=player_ids,
            user=self.player.type,
            input_type="int",
            message="Enter player id to trade with: ",
        ).process()
        trade_partner = players[choice]
        
        # Select resource to give
        resource_to_give = self._select_resource_to_give()
        
        # Select resource to receive
        resource_to_receive = self._select_resource_to_receive(trade_partner)
        
        # Perform the trade
        self._execute_player_trade(trade_partner, resource_to_give, resource_to_receive)
    
    def _select_resource_to_give(self) -> str:
        """
        Select a resource to give in a trade.

        Returns:
            str: The name of the resource to give.
        """
        return InputHandler(
            value_range=["brick", "wood", "sheep", "wheat", "ore"],
            user=self.player.type,
            input_type="str",
            message="Enter resource to give: ",
        ).process()
    
    def _select_resource_to_receive(self, trade_partner) -> str:
        """
        Select a resource to receive in a trade.

        Args:
            trade_partner: The player to trade with.

        Returns:
            str: The name of the resource to receive.
        """
        return InputHandler(
            value_range=["brick", "wood", "sheep", "wheat", "ore"],
            user=self.player.type,
            input_type="str",
            message="Enter resource to receive: ",
        ).process()
    
    def _execute_player_trade(
        self, trade_partner, resource_to_give: str, resource_to_receive: str
    ) -> None:
        """
        Execute a trade with another player.

        Args:
            trade_partner: The player to trade with.
            resource_to_give (str): The resource to give.
            resource_to_receive (str): The resource to receive.

        Returns:
            None
        """
        # Check if the player has enough of the resource to give
        if getattr(self.player.resources, resource_to_give).count > 0:
            # Check if the trade partner has enough of the resource to receive
            if getattr(trade_partner.resources, resource_to_receive).count > 0:
                # Execute the trade
                getattr(self.player.resources, resource_to_give).count -= 1
                getattr(self.player.resources, resource_to_receive).count += 1
                getattr(trade_partner.resources, resource_to_give).count += 1
                getattr(trade_partner.resources, resource_to_receive).count -= 1
                print(
                    f"Trade successful! You gave 1 {resource_to_give} and received 1 {resource_to_receive}"
                )
            else:
                print(
                    f"Trade partner does not have enough {resource_to_receive} to trade."
                )
        else:
            print(f"You do not have enough {resource_to_give} to trade.")
    
    def bank_trade(self, board: Board) -> None:
        """
        Perform a trade with the bank or a port.

        Args:
            board (Board): The game board.

        Returns:
            None
        """
        # Get port ratios for the player
        port_ratios = self._get_port_ratios(board)
        
        # Select resource to give and the amount
        resource_to_give, amount = self._select_resource_and_amount_to_give(port_ratios)
        
        # Select resource to receive
        resource_to_receive = self._select_resource_to_receive_from_bank()
        
        # Execute the bank trade
        self._execute_bank_trade(resource_to_give, amount, resource_to_receive)
    
    def _get_port_ratios(self, board: Board) -> Dict[str, int]:
        """
        Get the port trade ratios for the player.

        Args:
            board (Board): The game board.

        Returns:
            Dict[str, int]: A dictionary mapping resource names to their trade ratios.
        """
        # Implementation details for getting port ratios
        return {"brick": 4, "wood": 4, "sheep": 4, "wheat": 4, "ore": 4}
    
    def _select_resource_and_amount_to_give(self, port_ratios: Dict[str, int]) -> tuple:
        """
        Select a resource and the amount to give in a bank trade.

        Args:
            port_ratios (Dict[str, int]): The port trade ratios for the player.

        Returns:
            tuple: A tuple containing the resource name and the amount to give.
        """
        resource_to_give = InputHandler(
            value_range=["brick", "wood", "sheep", "wheat", "ore"],
            user=self.player.type,
            input_type="str",
            message="Enter resource to give: ",
        ).process()
        amount = port_ratios[resource_to_give]
        return resource_to_give, amount
    
    def _select_resource_to_receive_from_bank(self) -> str:
        """
        Select a resource to receive from the bank.

        Returns:
            str: The name of the resource to receive.
        """
        return InputHandler(
            value_range=["brick", "wood", "sheep", "wheat", "ore"],
            user=self.player.type,
            input_type="str",
            message="Enter resource to receive: ",
        ).process()
    
    def _execute_bank_trade(
        self, resource_to_give: str, amount: int, resource_to_receive: str
    ) -> None:
        """
        Execute a trade with the bank.

        Args:
            resource_to_give (str): The resource to give.
            amount (int): The amount of the resource to give.
            resource_to_receive (str): The resource to receive.

        Returns:
            None
        """
        # Check if the player has enough of the resource to give
        if getattr(self.player.resources, resource_to_give).count >= amount:
            # Execute the trade
            getattr(self.player.resources, resource_to_give).count -= amount
            getattr(self.player.resources, resource_to_receive).count += 1
            print(
                f"Trade successful! You gave {amount} {resource_to_give} and received 1 {resource_to_receive}"
            )
        else:
            print(f"You do not have enough {resource_to_give} to trade.")
