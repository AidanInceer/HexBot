class Resources:
    def __init__(self):
        self.resources = {
            "brick": 0,
            "ore": 0,
            "sheep": 0,
            "wheat": 0,
            "wood": 0,
        }

    def __getitem__(self, key):
        return self.resources[key]

    def __setitem__(self, key, value):
        self.resources[key] = value
