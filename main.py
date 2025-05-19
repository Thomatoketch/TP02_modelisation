from Classes.Mesh import *
from function import *
from butterfly_subdivision import *
from loop_subdivision import *

mesh_test = Mesh()
mesh_test.read_file("Hexa.obj")
mesh_test.info()

if input("Afficher les détails ? (y/n) : ") == "y":
    print_mesh_details(mesh_test)

if input("Afficher les arêtes de bord ? (y/n) : ") == "y":
    print_edge(mesh_test)

choice = input("Quel schéma de subdivision ? (loop / butterfly / none) : ").strip().lower()
if choice == "loop":
    mesh_test = loop_subdivision(mesh_test, iterations=1)
elif choice == "butterfly":
    mesh_test = butterfly_subdivision(mesh_test, iterations=1)

if input("Afficher dans Polyscope ? (y/n) : ") == "y":
    mesh_test.visualize_faces()
