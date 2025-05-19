from Classes.Vertex import *
from Classes.HalfEdge import *
from Classes.Face import *
import polyscope as ps
import numpy as np
import random

class Mesh :
    def __init__(self):
        self.vertex : List[Vertex] = []
        self.half_edges : List[HalfEdge] = []
        self.faces : List[Face] = []
        self.faces_idx = []

    def read_file(self, filename : str):
        faces_idx = []
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith("v "):
                    _, x, y, z = line.split()
                    self.vertex.append(Vertex(float(x), float(y), float(z)))
                elif line.startswith("f "):
                    idx = [int(i) - 1 for i in line.split()[1:]]
                    self.faces_idx.append(idx)
        self.constr_graph()

    def constr_graph(self):
        edge_map: Dict[Tuple[int, int], HalfEdge] = {}

        for face_id, verts in enumerate(self.faces_idx):
            for vid in verts:
                if not (0 <= vid < len(self.vertex)):
                    raise IndexError(f"Vertex index {vid} hors bornes (face {face_id})")

            face = Face()
            prev_he = None
            first_he = None

            pairs = list(zip(verts, verts[1:])) + [(verts[-1], verts[0])]

            for src_idx, dst_idx in pairs:
                he = HalfEdge()
                he.facette = face
                he.target_vertex = self.vertex[dst_idx]

                src_vertex = self.vertex[src_idx]
                if src_vertex.half_edge_out is None:
                    src_vertex.half_edge_out = he

                rev_key = (dst_idx, src_idx)
                if rev_key in edge_map:
                    twin_he = edge_map[rev_key]
                    he.twin = twin_he
                    twin_he.twin = he

                edge_map[(src_idx, dst_idx)] = he
                self.half_edges.append(he)

                if prev_he is not None:
                    prev_he.next = he
                    he.prev = prev_he
                else:
                    first_he = he

                prev_he = he

            prev_he.next = first_he
            first_he.prev = prev_he

            face.half_edge = first_he
            self.faces.append(face)

    def info(self):
        """Affiche le nombre de sommets, faces et demi-arêtes"""
        print(f"Sommets    : {len(self.vertex)}")
        print(f"Faces      : {len(self.faces)}")
        print(f"Half-Edges : {len(self.half_edges)}")

        print("=== Voisins immédiats ===")
        for i in [random.randint(0, len(self.vertex) - 1) for _ in range(3)]:
            vertex = self.vertex[i]
            neighbors = set()
            neighbors.add(self.vertex.index(vertex.half_edge_out.prev.target_vertex))
            neighbors.add(self.vertex.index(vertex.half_edge_out.next.target_vertex))

            print(f"Sommet {i} : voisins = {neighbors}")

        print("=== Sommet des Faces ===")
        for i, f in enumerate(self.faces):
            he_start = f.half_edge
            he = he_start
            verts = []
            while True:
                verts.append(self.vertex.index(he.target_vertex))
                he = he.next
                if he == he_start:
                    break
            print(f"{i}: vertices = {verts}")

    def visualize_faces(self):
        vertices = np.array([[v.x, v.y, v.z] for v in self.vertex])
        faces = np.array(self.faces_idx)

        ps.init()
        ps_mesh = ps.register_surface_mesh("Maillage", np.array(vertices), np.array(faces))

        boundary_faces = set()
        for he in self.half_edges:
            if he.twin is None:
                boundary_faces.add(self.faces.index(he.facette))

        M = faces.shape[0]
        face_colors = np.ones((M, 3)) * 0.8
        for f in boundary_faces:
            face_colors[f] = [1.0, 0.0, 0.0]

        ps_mesh.add_color_quantity(
            "Frontières en rouge",  # nom
            face_colors,  # (M,3)
            defined_on='faces',  # <- IMPORTANT
            enabled=True
        )

        # Affichage
        ps.show()