def print_mesh_details(mesh):
    """Affiche toutes les positions de sommets, les demi-arêtes et les faces."""
    # Sommets
    print("=== Vertices ===")
    for i, v in enumerate(mesh.vertex):
        print(f"{i}: X = {v.x}, Y = {v.x}, Z = {v.x}")

    # Half-Edges
    print("=== Half-Edges ===")
    for i, he in enumerate(mesh.half_edges):
        dest = mesh.vertex.index(he.target_vertex) if he.target_vertex else None
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
            verts.append(mesh.vertex.index(he.target_vertex))
            he = he.next
            if he == he_start:
                break
        print(f"{i}: vertices = {verts}")


def print_edge(mesh):
    edge = []
    for i in range(len(mesh.half_edges)):
        if mesh.half_edges[i].twin is None:
            edge.append(i)
    return edge