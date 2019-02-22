class Vertex:
    def __init__(self):
        self.settlement = None
        self.owner = None
        self.location = None # tuple (i, j, k) where i, j are the indices of an adjacent tile
                             # and k is the vertex's index in this tile's vertex list

    def serialize(self):
        ret_dict = {}
        ret_dict['settlement'] = 0 if self.settlement is None else self.settlement.value
        ret_dict['owner'] = self.owner.name
        ret_dict['location'] = self.location
        return ret_dict
