from collections import defaultdict

class Player:
    def __init__(self, name):
        self.name = name
        self.resources = defaultdict(int)
        self.development_cards = []

    def serialize(self):
        ret_dict = {}
        ret_dict['name'] = self.name
        ret_dict['resources'] = {k.value : v for k,v in self.resources.items()}
        return ret_dict
