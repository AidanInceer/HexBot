from src.interface.protocols import DisplayHandlerProtocol
from typing import Any


class TerminalDisplayHandler:
    def message(self, msg: str) -> None:
        print(msg)

    def update_board(self, board_state: Any) -> None:
        # Assuming board_state has a display method or we call it
        if hasattr(board_state, "display"):
            # board_state.display() is what prints in the terminal version,
            # but the Board class prints directly. We need to tell the board to return string or just print here.
            # For now, we will rely on Refactoring Board to return string.
            print(board_state.display_str())
