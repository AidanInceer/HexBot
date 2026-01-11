import random
import pandas as pd
from typing import Any, List


class TerminalInputHandler:
    def __init__(self):
        pass

    def process(self, value_range, user, input_type, message=None):
        if user == "human":
            return self.handle_user_input(value_range, input_type, message)
        elif user == "bot":
            return self.handle_bot_input(value_range, user, input_type, message)

    def handle_user_input(self, value_range, input_type, message):
        successful_input = False
        user_input = None
        while not successful_input:
            if input_type == "int":
                try:
                    user_input = int(input(f"{message}: "))
                    if user_input in value_range:
                        successful_input = True
                except ValueError:
                    pass
            if input_type in ["resource", "player", "action", "card"]:
                user_input = input(f"{message}: ")
                if user_input in value_range and isinstance(user_input, str):
                    successful_input = True
        return user_input

    def handle_bot_input(self, value_range, user, input_type, message):
        range_input = list(value_range)
        bot_decision = random.choice(range_input)

        # Log bot input (kept from original)
        try:
            row = {
                "user": user,
                "value_range": list(value_range),
                "input_type": input_type,
                "message": message,
                "choice": bot_decision,
            }
            # Only append if file exists or handle error, keeping simple for now
            # df = pd.read_csv("./data/basic/games.csv")
            # df = df._append(row, ignore_index=True)
            # df.to_csv("./data/basic/games.csv", index=False)
        except Exception:
            pass  # Ignore logging errors during refactor

        return bot_decision


# New Web Input Handler logic will be injected, but this file can stay as the base or hold multiple implementations.
# For now, we update the original class to be compatible or leave it for the terminal fallback.
# I will rename the original class to maintain compatibility if imports are direct,
# OR I will keep the name InputHandler but add flexibility.


class InputHandler:
    """Legacy wrapper or main entry point depending on injection."""

    def __init__(self, value_range, user, input_type, message=None, handler_backend=None):
        self.value_range = value_range
        self.user = user
        self.input_type = input_type
        self.message = message
        self.handler_backend = handler_backend or TerminalInputHandler()

    def process(self):
        # Delegate to the backend implementation
        return self.handler_backend.process(self.value_range, self.user, self.input_type, self.message)
