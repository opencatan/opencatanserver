import sys

class Vertex:
    def __init__(self):
        self.settlement = None
        self.owner = None
        self.port = None #tbd how to represent ports
        self.adjacent_tiles = [] #list of adjacent tiles

class Graph:
    def __init__(self):
        self.vertices = []
        self.A = None #adjaceny matrix

    def insert(self, vertex):
        self.vertices.append(vertex)
        if not self.A:
            self.A = [[None]]
        else:
            for row in self.A:
                row.append(None)
            self.A.append([None] * (len(self.A) + 1))

    def connect(self, v1, v2, data):
        try:
            i = self.vertices.index(v1)
            j = self.vertices.index(v2)
        except ValueError:
            print("vertex not found", file=sys.stderr)
            return
        # #ensure i < j
        # if i > j:
        #     i, j = j, i
        #TODO:  more elegant graph
        self.A[i][j] = data
        self.A[j][i] = data

    def connected(self, v1, v2):
        try:
            i = self.vertices.index(v1)
            j = self.vertices.index(v2)
        except ValueError:
            print("vertex not found", file=sys.stderr)
            return
        return self.A[i][j] == data

    def adjacent_edges(self, vertex):
        try:
            i = self.vertices.index(vertex)
        except ValueError:
            print("vertex not found", file=sys.stderr)
            return
        return [e for e in self.A[i] if e is not None]

    #very untested
    def adjacent_vertices(self, vertex):
        try:
            i = self.vertices.index(vertex)
        except ValueError:
            print("vertex not found", file=sys.stderr)
            return
        indices = [ind for ind, e in enumerate(self.A[i]) if e is not None]
        return [self.vertices[ind] for ind in indices]
