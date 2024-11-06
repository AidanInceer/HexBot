import random
import time


class InputHandler:
    def __init__(self, value_range, user, input_type, message=None):
        self.value_range = value_range
        self.user = user
        self.input_type = input_type
        self.message = message

    def process(self):
        if self.user == "human":
            output = self.handle_user_input()
        elif self.user == "bot":
            output = self.handle_bot_input()
        return output

    def handle_user_input(self):
        successful_input = False
        while not successful_input:
            if self.input_type == "int":
                user_input = int(input(f"{self.message}: "))
                if user_input in self.value_range and isinstance(user_input, int):
                    successful_input = True
            if self.input_type in ["resource", "player", "action", "card"]:
                user_input = input(f"{self.message}: ")
                if user_input in self.value_range and isinstance(user_input, str):
                    successful_input = True

        return user_input

    def handle_bot_input(self):
        range_input = list(self.value_range)
        bot_desicion = random.choice(range_input)
        # append bot input to log csv for training, [ID, input, type]
        # new csv file for each game
        return bot_desicion
