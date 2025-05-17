from Classes.Mesh import *
from function import *

mesh_test = Mesh()
mesh_test.read_file("Hexa.obj")
mesh_test.info()
#mesh_test.visualize_faces("Hexa.obj")

if input("Afficher les details (y/n) : ") == "y":
    print_mesh_details(mesh_test)

if input("Afficher les arêtes de bord (y/n) : ") == "y":
    print_edge(mesh_test)


