from Classes.Mesh import *
from function import *

mesh_test = Mesh()
mesh_test.read_file("Cube.obj")
mesh_test.info()
#mesh_test.visualize_faces("Hexa.obj")

if input("Afficher les details (y/n) : ") == "y":
    print_mesh_details(mesh_test)

if input("Afficher les arêtes de bord (y/n) : ") == "y":
    [print(f"Half-Edge: {x}") for x in print_edge(mesh_test)]

if input("Afficher le dessin de l'objet (y/n) : ") == "y":
    mesh_test.visualize_faces("Cube.obj")


