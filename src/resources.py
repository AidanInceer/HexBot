class Resources:
    def __init__(self):
        self.resources = {
            "brick": 4,
            "ore": 0,
            "sheep": 2,
            "wheat": 2,
            "wood": 4,
        }

    def __getitem__(self, key):
        return self.resources[key]

    def __setitem__(self, key, value):
        self.resources[key] = value
