import numpy as np
from Classes.Mesh import Mesh
from Classes.Vertex import Vertex
from Classes.HalfEdge import HalfEdge
from Classes.Face import Face

def butterfly_subdivision(mesh: Mesh, iterations: int = 1) -> Mesh:
    for _ in range(iterations):
        edge_vertex_map = {}
        id_map = {}
        new_mesh = Mesh()

        for he in mesh.half_edges:
            v1 = he.prev.target_vertex
            v2 = he.target_vertex
            key = tuple(sorted((id(v1), id(v2))))
            if key in edge_vertex_map:
                continue

            if he.twin and he.next and he.twin.next:
                f1 = he.next.target_vertex
                f2 = he.twin.next.target_vertex
                pos = (
                    0.5 * (np.array([v1.x, v1.y, v1.z]) + np.array([v2.x, v2.y, v2.z])) +
                    0.125 * (np.array([f1.x, f1.y, f1.z]) + np.array([f2.x, f2.y, f2.z]))
                )
            else:
                pos = 0.5 * (np.array([v1.x, v1.y, v1.z]) + np.array([v2.x, v2.y, v2.z]))

            new_v = Vertex(*pos)
            edge_vertex_map[key] = new_v

        for face in mesh.faces:
            he1 = face.half_edge
            he2 = he1.next
            he3 = he2.next

            v0 = he1.prev.target_vertex
            v1 = he1.target_vertex
            v2 = he2.target_vertex

            def get_mid_vertex(a, b):
                key = tuple(sorted((id(a), id(b))))
                return edge_vertex_map[key]

            vm0 = get_mid_vertex(v0, v1)
            vm1 = get_mid_vertex(v1, v2)
            vm2 = get_mid_vertex(v2, v0)

            for v in [v0, v1, v2, vm0, vm1, vm2]:
                if id(v) not in id_map:
                    id_map[id(v)] = len(new_mesh.vertex)
                    new_mesh.vertex.append(Vertex(v.x, v.y, v.z))

            idx = id_map
            faces = [
                [idx[id(v0)], idx[id(vm0)], idx[id(vm2)]],
                [idx[id(vm0)], idx[id(v1)], idx[id(vm1)]],
                [idx[id(vm1)], idx[id(v2)], idx[id(vm2)]],
                [idx[id(vm0)], idx[id(vm1)], idx[id(vm2)]]
            ]

            for f in faces:
                v_a, v_b, v_c = f
                face = Face()
                he1 = HalfEdge()
                he2 = HalfEdge()
                he3 = HalfEdge()

                he1.target_vertex = new_mesh.vertex[v_b]
                he2.target_vertex = new_mesh.vertex[v_c]
                he3.target_vertex = new_mesh.vertex[v_a]

                he1.next = he2
                he2.next = he3
                he3.next = he1

                he1.prev = he3
                he2.prev = he1
                he3.prev = he2

                he1.face = face
                he2.face = face
                he3.face = face

                face.half_edge = he1
                new_mesh.half_edges.extend([he1, he2, he3])
                new_mesh.faces.append(face)

                for he in [he1, he2, he3]:
                    src_idx = new_mesh.vertex.index(he.prev.target_vertex)
                    if new_mesh.vertex[src_idx].half_edge_out is None:
                        new_mesh.vertex[src_idx].half_edge_out = he

        mesh = new_mesh

    return mesh
