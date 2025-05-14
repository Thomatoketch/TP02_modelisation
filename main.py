from Classes.Mesh import *

mesh_test = Mesh()
mesh_test.read_file("cube.obj")
mesh_test.verification()

def vertex_neighbors(v):
    neighbors = []
    start = v.half_edge_out
    he = start
    while True:
        neighbors.append(he.destination)
        he = he.twin.next if he.twin else None
        if he is None or he == start:
            break
    return neighbors

# affichage des voisins pour les trois premiers sommets
for i, v in enumerate(mesh_test.vertex[:3]):
    neigh = vertex_neighbors(v)
    print(f"Voisins du sommet {i} : {[mesh_test.vertex.index(n) for n in neigh]}")

# sommets d'une face donnée
for i, f in enumerate(mesh_test.faces[:2]):
    he_start = f.edge
    he = he_start
    verts = []
    while True:
        verts.append(mesh_test.vertex.index(he.destination))
        he = he.next
        if he == he_start:
            break
    print(f"Face {i} : {verts}")

def print_mesh_details(mesh):
    """Affiche toutes les positions de sommets, les demi-arêtes et les faces."""
    # Sommets
    print("=== Vertices ===")
    for i, v in enumerate(mesh.vertex):
        print(f"{i}: X = {v.x}, Y = {v.x}, Z = {v.x}")

    # Half-Edges
    print("=== Half-Edges ===")
    for i, he in enumerate(mesh.half_edges):
        dest = mesh.vertex.index(he.destination) if he.destination else None
        twin = mesh.half_edges.index(he.twin) if he.twin else None
        nxt  = mesh.half_edges.index(he.next) if he.next else None
        prev = mesh.half_edges.index(he.prev) if he.prev else None
        face_idx = mesh.faces.index(he.face) if he.face else None
        print(
            f"{i}: dest={dest}, twin={twin}, next={nxt}, prev={prev}, face={face_idx}"
        )

    # Faces
    print("=== Faces ===")
    for i, f in enumerate(mesh.faces):
        he_start = f.edge
        he = he_start
        verts = []
        while True:
            verts.append(mesh.vertex.index(he.destination))
            he = he.next
            if he == he_start:
                break
        print(f"{i}: vertices = {verts}")


if input("Est ce que vous voulez afficher les details : ") == "y":
    print_mesh_details(mesh_test)