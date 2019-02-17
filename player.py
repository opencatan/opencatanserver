import sys

class Player:
    def __init__(self, name):
        self.name = name
        self.resources = {
                    'wheat': 0,
                    'ore': 0,
                    'sheep': 0,
                    'brick': 0,
                    'wood': 0
                    }
        self.development_cards = []

    def serialize(self):
        ret_dict = {}
        ret_dict['name'] = self.name
        ret_dict['resources'] = self.resources
        return ret_dict
