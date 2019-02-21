import sys

class Player:
    def __init__(self, name):
        self.name = name
        self.resources = { #test values
                    'wheat': 1,
                    'ore': 1,
                    'sheep': 1,
                    'brick': 1,
                    'wood': 1
                    }
        self.development_cards = []

    def serialize(self):
        ret_dict = {}
        ret_dict['name'] = self.name
        ret_dict['resources'] = self.resources
        return ret_dict
