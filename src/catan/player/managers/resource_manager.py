from __future__ import annotations

from src.catan.resources.resources import Resources


class ResourceManager:
    """Manages a player's resources and resource-related operations."""
    
    def __init__(self, resources=None):
        self.resources = resources or Resources()
    
    def deduct_settlement_cost(self) -> None:
        """
        Deducts the cost of a settlement from the player's resources.
        
        Returns:
            None
        """
        self.resources.brick.count -= 1
        self.resources.wood.count -= 1
        self.resources.sheep.count -= 1
        self.resources.wheat.count -= 1
    
    def deduct_city_cost(self) -> None:
        """
        Deducts the cost of a city from the player's resources.
        
        Returns:
            None
        """
        self.resources.ore.count -= 3
        self.resources.wheat.count -= 2
    
    def deduct_road_cost(self) -> None:
        """
        Deducts the cost of a road from the player's resources.
        
        Returns:
            None
        """
        self.resources.brick.count -= 1
        self.resources.wood.count -= 1
    
    def deduct_dev_card_cost(self) -> None:
        """
        Deducts the cost of a development card from the player's resources.
        
        Returns:
            None
        """
        self.resources.sheep.count -= 1
        self.resources.wheat.count -= 1
        self.resources.ore.count -= 1
    
    def has_resources_for_settlement(self) -> bool:
        """
        Checks if the player has enough resources to build a settlement.
        
        Returns:
            bool: True if the player has enough resources, False otherwise.
        """
        return (
            self.resources.brick.count >= 1
            and self.resources.wood.count >= 1
            and self.resources.sheep.count >= 1
            and self.resources.wheat.count >= 1
        )
    
    def has_resources_for_city(self) -> bool:
        """
        Checks if the player has enough resources to build a city.
        
        Returns:
            bool: True if the player has enough resources, False otherwise.
        """
        return self.resources.ore.count >= 3 and self.resources.wheat.count >= 2
    
    def has_resources_for_road(self) -> bool:
        """
        Checks if the player has enough resources to build a road.
        
        Returns:
            bool: True if the player has enough resources, False otherwise.
        """
        return self.resources.brick.count >= 1 and self.resources.wood.count >= 1
    
    def has_resources_for_dev_card(self) -> bool:
        """
        Checks if the player has enough resources to buy a development card.
        
        Returns:
            bool: True if the player has enough resources, False otherwise.
        """
        return (
            self.resources.sheep.count >= 1
            and self.resources.wheat.count >= 1
            and self.resources.ore.count >= 1
        )
    
    def total_resources(self) -> int:
        """
        Calculates the total number of resources the player has.
        
        Returns:
            int: The total number of resources.
        """
        return (
            self.resources.brick.count
            + self.resources.wood.count
            + self.resources.sheep.count
            + self.resources.wheat.count
            + self.resources.ore.count
        )
    
    def discard_resources(self, total: int) -> None:
        """
        Discards a specified number of resources from the player.
        
        Args:
            total (int): The total number of resources to discard.
            
        Returns:
            None
        """
        # Implementation details for discarding resources
        pass
