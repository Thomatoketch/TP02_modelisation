import HalfEdge

class Vertex :
    def __init__(self, x : float, y : float, z : float, half_edge_out : HalfEdge):
        self.x = x
        self.y = y
        self.z = z
        self.half_edge_out = half_edge_out