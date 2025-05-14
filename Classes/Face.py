from Classes.HalfEdge import *

class Face :
    def __init__(self):
        self.half_edge : HalfEdge = None

    def info(self):
        print(f'Index: {self.index}, HalgEdge : {self.half_edge.info()}')