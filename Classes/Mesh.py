import Vertex
import HalfEdge
import Face

class Mesh :

    lines = []

    def __init__(self, vertex : list[Vertex], half_edge : list[HalfEdge], face : list[Face]):
        self.vertex = vertex
        self.half_edge = half_edge
        self.face = face

    @staticmethod
    def read_file(filename : str):
        with open(filename, 'r') as file:
            lines = file.readlines()

    def constr_graph(self, ):