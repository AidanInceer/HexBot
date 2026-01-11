
import random
from typing import Any, List
from src.interface.protocols import DisplayHandlerProtocol
from src.interface.web.bridge import GameBridge

class WebDisplayHandler:
    """
    Implements DisplayHandlerProtocol to route game output to the web interface via GameBridge.
    """
    def __init__(self, bridge: GameBridge) -> None:
        self.bridge = bridge

    def message(self, msg: str) -> None:
        self.bridge.push_msg(msg)

    def update_board(self, board: Any) -> None:
        self.bridge.push_board_update(board)


class WebInputHandler:
    """
    Implements InputHandler logic for the web interface.
    Delegates user input to the GameBridge (which prompts the UI).
    Handles 'bot' input automatically.
    """
    def __init__(self, bridge: GameBridge) -> None:
        self.bridge = bridge

    def process(
        self,
        value_range: List[Any],
        user: str,
        input_type: str,
        message: str | None = None,
    ) -> Any:
        if user == "bot":
            # Simple bot logic: choose random valid option
            # In a real scenario, this might call a sophisticated Bot Agent.
            if not value_range:
                return None
            return random.choice(list(value_range))
        
        # For human players, request input via the bridge
        return self.bridge.request_input(value_range, input_type, str(message))
