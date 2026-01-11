
import queue
from typing import Any, Tuple, Dict, Optional

class GameBridge:
    """
    Acts as a synchronized bridge between the Game Thread and the UI Thread (Main Thread).
    """

    def __init__(self) -> None:
        # Queue for messages and board updates from Game -> UI
        self.display_queue: queue.Queue[Tuple[str, Any]] = queue.Queue()
        
        # Queue for requests from Game -> UI (e.g., "Ask user for input")
        self.input_request_queue: queue.Queue[Dict[str, Any]] = queue.Queue()
        
        # Queue for responses from UI -> Game (e.g., "User selected 'Build New Road'")
        self.input_response_queue: queue.Queue[Any] = queue.Queue()

    def push_msg(self, msg: str) -> None:
        """Push a text message to the UI log."""
        self.display_queue.put(("msg", msg))

    def push_board_update(self, board: Any) -> None:
        """Push a board state update to the UI."""
        # Note: In a production app, we might want to deepcopy or serialize the board 
        # to avoid thread-safety issues with shared mutable state. 
        # For now, we pass the reference as per existing logic.
        self.display_queue.put(("board", board))

    def request_input(self, value_range: list, input_type: str, message: str) -> Any:
        """
        Blocking call from Game Thread: Sends request to UI and waits for response.
        """
        request_data = {
            "value_range": list(value_range),
            "input_type": input_type,
            "message": message
        }
        self.input_request_queue.put(request_data)
        
        # Block until the UI thread puts a response into the response queue
        return self.input_response_queue.get()
