from Classes.HalfEdge import *
from Classes.Face import *

class Vertex :
    def __init__(self, x : float, y : float, z : float):
        self.x : float = x
        self.y : float = y
        self.z : float = z
        self.half_edge_out :  HalfEdge = None
