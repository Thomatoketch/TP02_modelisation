from Classes.Vertex import *
from Classes.Face import *

class HalfEdge :
    def __init__(self):
        self.target_vertex: Vertex = None
        self.twin: HalfEdge = None
        self.next: HalfEdge = None
        self.prev: HalfEdge = None
        self.facette: Face = None