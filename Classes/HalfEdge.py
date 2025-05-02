import Vertex
import Face

class HalfEdge :
    def __init__(self, vertex : Vertex, twin : Vertex, next, prev, facette : Face):
        self.vertex = vertex
        self.twin = twin
        self.next = next
        self.prev = prev
        self.facette = facette