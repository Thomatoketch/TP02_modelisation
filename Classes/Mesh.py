from Classes.Vertex import *
from Classes.HalfEdge import *
from Classes.Face import *

class Mesh :
    def __init__(self):
        self.vertex : list[Vertex] = []
        self.half_edges : list[HalfEdge] = []
        self.faces : list[Face] = []

    def read_file(self, filename : str):
        faces_idx = []
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith("v "):
                    _, x, y, z = line.split()
                    self.vertex.append(Vertex(float(x), float(y), float(z)))
                elif line.startswith("f "):
                    idx = [int(i) - 1 for i in line.split()[1:]]
                    faces_idx.append(idx)
        self.constr_graph(faces_idx)

    def constr_graph(self, faces_idx):
        edge_dict = {}
        for idx in faces_idx:
            face = Face()
            prev_he = None
            first_he = None
            k = len(idx)
            for i in range(k):
                he = HalfEdge()
                he.face = face
                he.destination = self.vertex[idx[(i + 1) % k]]
                src = self.vertex[idx[i]]
                if src.half_edge_out is None:
                    src.half_edge_out = he
                key = (idx[i], idx[(i + 1) % k])
                edge_dict[key] = he
                self.half_edges.append(he)
                if prev_he:
                    prev_he.next = he
                    he.prev = prev_he
                else:
                    first_he = he
                prev_he = he
            prev_he.next = first_he
            first_he.prev = prev_he
            face.edge = first_he
            self.faces.append(face)

        # appariement des twins
        for (i, j), he in edge_dict.items():
            twin = edge_dict.get((j, i))
            if twin:
                he.twin = twin
                twin.twin = he

    def verification(self):
        """Affiche le nombre de sommets, faces et demi-arêtes"""
        print(f"Sommets    : {len(self.vertex)}")
        print(f"Faces      : {len(self.faces)}")
        print(f"Half-Edges : {len(self.half_edges)}")
        """[v.info() for v in self.vertex]
        [f.info() for f in self.face]
        [v.info() for v in self.vertex]"""

