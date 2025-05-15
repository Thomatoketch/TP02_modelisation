from Classes.Vertex import *
from Classes.HalfEdge import *
from Classes.Face import *
import polyscope as ps
import numpy as np

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

    def vertex_neighbors(self, v):
        neighbors = []
        start = v.half_edge_out
        he = start
        while True:
            neighbors.append(he.destination)
            he = he.twin.next if he.twin else None
            if he is None or he == start:
                break
        return neighbors

    def info(self):
        """Affiche le nombre de sommets, faces et demi-arêtes"""
        print(f"Sommets    : {len(self.vertex)}")
        print(f"Faces      : {len(self.faces)}")
        print(f"Half-Edges : {len(self.half_edges)}")

        # affichage des voisins pour les trois premiers sommets
        for i, v in enumerate(self.vertex[:3]):
            neighbors = self.vertex_neighbors(v)
            print(f"Voisins du sommet {i} : {[self.vertex.index(n) for n in neighbors]}")

        # sommets d'une face donnée
        for i, f in enumerate(self.faces[:2]):
            he_start = f.edge
            he = he_start
            verts = []
            while True:
                verts.append(self.vertex.index(he.destination))
                he = he.next
                if he == he_start:
                    break
            print(f"Face {i} : {verts}")

    def visualize_faces(self, filename : str):
        vertices = []
        faces = []
        with open(filename, 'r') as file:
            for line in file:
                toks = line.split()
                if line.startswith("v "):
                    vertices.append([float(v) for v in toks[1:]])
                elif line.startswith("f "):
                    face = [int(v.split('/')[0]) - 1 for v in toks[1:]]
                    faces.append(face)
        # Initialisation de Polyscope
        ps.init()

        # Extraction des coordonnées des sommets

        # Ajout du maillage à Polyscope
        ps.register_surface_mesh("Maillage", np.array(vertices), np.array(faces))

        # Affichage
        ps.show()