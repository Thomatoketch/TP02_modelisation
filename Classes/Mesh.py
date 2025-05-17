from Classes.Vertex import *
from Classes.HalfEdge import *
from Classes.Face import *
import polyscope as ps
import numpy as np

class Mesh :
    def __init__(self):
        self.vertex : List[Vertex] = []
        self.half_edges : List[HalfEdge] = []
        self.faces : List[Face] = []

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
        edge_map: Dict[Tuple[int, int], HalfEdge] = {}

        for face_id, verts in enumerate(faces_idx):
            # Validation des indices
            for vid in verts:
                if not (0 <= vid < len(self.vertex)):
                    raise IndexError(f"Vertex index {vid} hors bornes (face {face_id})")

            face = Face()
            prev_he = None
            first_he = None

            pairs = list(zip(verts, verts[1:])) + [(verts[-1], verts[0])]
            print(pairs)

            for src_idx, dst_idx in pairs:
                he = HalfEdge()
                he.face = face
                he.destination = self.vertex[dst_idx]

                src_vertex = self.vertex[src_idx]
                if src_vertex.half_edge_out is None:
                    src_vertex.half_edge_out = he

                # Appariement immédiat des twins
                rev_key = (dst_idx, src_idx)
                print(rev_key)
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

            # Ferme la chaîne circulaire des demi-arêtes
            prev_he.next = first_he
            first_he.prev = prev_he

            face.edge = first_he
            self.faces.append(face)
        print(edge_map)

    def info(self):
        """Affiche le nombre de sommets, faces et demi-arêtes"""
        print(f"Sommets    : {len(self.vertex)}")
        print(f"Faces      : {len(self.faces)}")
        print(f"Half-Edges : {len(self.half_edges)}")

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