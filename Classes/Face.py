from Classes.HalfEdge import *

class Face :
    def __init__(self):
        self.half_edge : HalfEdge = None

    def calculate_normal(self):
        if len(self.vertices) >= 3:
            v1 = self.vertices[0]
            v2 = self.vertices[1]
            v3 = self.vertices[2]

            # Calcul des vecteurs
            vector1 = (v2.x - v1.x, v2.y - v1.y, v2.z - v1.z)
            vector2 = (v3.x - v1.x, v3.y - v1.y, v3.z - v1.z)

            # Produit vectoriel
            normal_x = vector1[1] * vector2[2] - vector1[2] * vector2[1]
            normal_y = vector1[2] * vector2[0] - vector1[0] * vector2[2]
            normal_z = vector1[0] * vector2[1] - vector1[1] * vector2[0]

            # Normalisation
            magnitude = math.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
            self.normal = (normal_x / magnitude, normal_y / magnitude, normal_z)