from Classes.Vertex import *
from Classes.Face import *

class HalfEdge :
    def __init__(self):
        self.target_vertex: Vertex = None
        self.twin: HalfEdge = None
        self.next: HalfEdge = None
        self.prev: HalfEdge = None
        self.facette: Face = None

    def info(self):
        print(f'target_vertex : {self.target_vertex.index}, twin:{self.twin.index}, next:{self.next.index}, prev:{self.prev.index}, facette:{self.facette}]')