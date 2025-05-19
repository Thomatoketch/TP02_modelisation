from Classes.HalfEdge import *

class Face :
    def __init__(self):
        self.half_edge : HalfEdge = None

    def compute_normal(self):
        # Supposons que self.half_edge pointe vers un HalfEdge de la face
        he1 = self.half_edge
        he2 = he1.next
        he3 = he2.next

        v1 = np.array([he1.origin.x, he1.origin.y, he1.origin.z])
        v2 = np.array([he2.origin.x, he2.origin.y, he2.origin.z])
        v3 = np.array([he3.origin.x, he3.origin.y, he3.origin.z])

        # Calcul des vecteurs
        vec1 = v2 - v1
        vec2 = v3 - v1

        # Produit vectoriel pour obtenir la normale
        normal = np.cross(vec1, vec2)
        # Normalisation
        norm = np.linalg.norm(normal)
        if norm != 0:
            normal = normal / norm
        self.normal = normal