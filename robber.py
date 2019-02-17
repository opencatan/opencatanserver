import sys

class Robber:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def serialize(self):
        ret_dict = {}
        ret_dict['row'] = self.row
        ret_dict['column'] = self.column
        return ret_dict
