import random


class InputHandler:
    def __init__(self, value_range, user, input_type, message):
        self.value_range = value_range
        self.user = user
        self.input_type = input_type
        self.message = message

    def process(self):
        if self.user == "human":  # TODO: add class types
            self.handle_user_input()
        elif self.user == "bot":  # TODO: add class types
            self.handle_bot_input()

    def handle_user_input(self):
        successful_input = False
        while successful_input:
            if self.input_type == "int":
                user_input = int(
                    input("Please enter a number between {self.value_range} and {}: ")
                )
                if user_input in self.value_range and isinstance(user_input, int):
                    successful_input = True
            if self.input_type == "resource":
                user_input = input(
                    f"Please input a resource from: {self.value_range}: "
                )
                if user_input in self.value_range and isinstance(user_input, str):
                    successful_input = True
            if self.input_type == "player":
                user_input = input(f"Please input a player from: {self.value_range}: ")
                if user_input in self.value_range and isinstance(user_input, str):
                    successful_input = True
            if self.input_type == "action":
                user_input = input(f"Please input an action from: {self.value_range}: ")
                if user_input in self.value_range and isinstance(user_input, str):
                    successful_input = True
            if self.input_type == "card":
                user_input = input(f"Please input a card from: {self.value_range}: ")
                if user_input in self.value_range and isinstance(user_input, str):
                    successful_input = True

        return user_input

    def handle_bot_input(self):
        bot_desicion = random.choice(self.value_range)
        # append bot input to log csv for training, [ID, input, type]
        # new csv file for each game

        return bot_desicion
