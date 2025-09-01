from pyglet.gl import GL_TRIANGLES
from pyglet.graphics import Batch, Group, ShaderProgram, VertexList


from sombra_engine.models import Mesh
from sombra_engine.primitives import (
    Material, SceneObject, Transform, VertexGroup
)


class Bone:
    def __init__(self, idx: int, name: str, transform: Transform):
        self.idx = idx
        self.name = name
        self.transform = transform
        self.children: list[Bone] = []


class SkeletalMesh(Mesh):

    def __init__(
        self,
        name: str,
        vertex_groups: dict[str, VertexGroup] = None,
        materials: dict[str, Material] = None,
        root_bone: Bone = None,
        mode: int = GL_TRIANGLES,
        batch: Batch = None,
        group: Group = None,
        program: ShaderProgram = None,
        transform: Transform = Transform(),
        parent: SceneObject = None
    ):
        super().__init__(
            name=name,
            vertex_groups=vertex_groups,
            materials=materials,
            mode=mode,
            batch=batch,
            group=group,
            program=program,
            transform=transform,
            parent=parent
        )
        self.root_bone = root_bone

    def create_vertex_lists(self) -> list[VertexList]:
        vlists = []

        for vg_name, vg in self.vertex_groups.items():
            (
                position_list, normal_list, tangent_list, tex_coords_list,
                bones_ids_list, weights_list
            ) = self.get_lists_for_vertex_group(vg_name)
            material_group = self.material_groups[vg.material.name]
            vl = self.program.vertex_list(
                len(vg.triangles) * 3, self.mode,
                batch=self.batch, group=material_group,
                position=('f', position_list),
                normal=('f', normal_list),
                tangent=('f', tangent_list),
                tex_coords=('f', tex_coords_list),
                bones_isds=('i', bones_ids_list),
                weights=('f', weights_list)
            )
            vlists.append(vl)
        return vlists

    def get_lists_for_vertex_group(self, vertex_group_name: str) -> tuple[
        list[float], list[float], list[float], list[float], list[int],
        list[float]
    ]:
        if vertex_group_name not in self.vertex_groups:
            raise KeyError(
                f"Couldn't find key {vertex_group_name} for vertex group in "
                f"mesh {self.name}"
            )
        position_list = []
        normal_list = []
        tangent_list = []
        tex_coords_list = []
        bones_ids_list = []
        weights_list = []

        for triangle in self.vertex_groups[vertex_group_name].triangles:
            for v in triangle.vertices:
                position_list += [v.position.x, v.position.y, v.position.z]
                normal_list += [v.normal.x, v.normal.y, v.normal.z]
                tangent_list += [v.tangent.x, v.tangent.y, v.tangent.z]
                tex_coords_list += [v.tex_coords.x, v.tex_coords.y]
                bones_ids_list += [*v.bones_ids]
                weights_list += [
                    v.weights.x, v.weights.y, v.weights.z, v.weights.w
                ]
        return (
            position_list, normal_list, tangent_list, tex_coords_list,
            bones_ids_list, weights_list
        )
