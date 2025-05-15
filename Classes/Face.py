from Classes.HalfEdge import *

class Face :
    def __init__(self):
        self.half_edge : HalfEdge = None

    def is_boundary(self):
        edge = self.half_edge
        while True:
            if edge.twin is None:  # Pas de demi-arête jumelle, donc frontière
                return True
            edge = edge.next
            if edge == self.half_edge:
                break
        return False