from typing import Protocol, Any, List


class DisplayHandlerProtocol(Protocol):
    def message(self, msg: str) -> None: ...

    def update_board(self, board_state: Any) -> None: ...


class InputHandlerProtocol(Protocol):
    def process(
        self,
        value_range: List[Any] | range,
        user: str,
        input_type: str,
        message: str | None = None,
    ) -> Any: ...
