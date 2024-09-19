from pyglet.gl import *
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram
from pyglet.graphics.vertexdomain import VertexList

from sombra_engine.graphics import MaterialGroup
from sombra_engine.primitives import (
    Material, SceneObject, Transform, Triangle,
    VertexGroup
)


def get_lists_for_triangles(triangles: list[Triangle]):
    position_list = []
    tex_coords_list = []
    normal_list = []
    for triangle in triangles:
        for v in triangle.vertices:
            position_list += [v.position.x, v.position.y, v.position.z]
            tex_coords_list += [v.tex_coords.x, v.tex_coords.y]
            normal_list += [v.normal.x, v.normal.y, v.normal.z]
    return position_list, tex_coords_list, normal_list


class Mesh:
    def __init__(
        self,
        name: str,
        vertex_groups: dict[str, VertexGroup] = None,
        materials: dict[str, Material] = None,
        mode: int = GL_TRIANGLES,
        batch: Batch = None,
        group: Group = None,
        program: ShaderProgram = None,
        transform: Transform = Transform(),
        parent: SceneObject = None
    ):
        self.name = name
        self.vertex_groups = vertex_groups
        self.materials = materials
        self.mode = mode
        self.batch = batch or pyglet.graphics.get_default_batch()
        self.group = group
        self.program = program or pyglet.graphics.get_default_shader()
        self.transform = transform
        self.parent = parent

        self.material_groups = self.create_material_groups()
        self.vertex_lists = self.create_vertex_lists()

    def create_material_groups(self) -> dict[str, MaterialGroup]:
        groups = {}
        for name, material in self.materials.items():
            new_group = MaterialGroup(
                material, self.program, order=0, parent=self.group
            )
            groups[name] = new_group
        return groups

    def create_vertex_lists(self) -> list[VertexList]:
        """
        This method creates a vertex list for each vertex group using the
        Shader Program that this Mesh currently has, and returns all
        of them in a list.

        Returns:
            list[IndexedVertexList]: The list with the newly created vertex
                lists.
        """
        vlists = []

        for vg in self.vertex_groups.values():
            (
                position_list, tex_coords_list, normal_list
            ) = get_lists_for_triangles(vg.triangles)
            material_group = self.material_groups[vg.material.name]
            vl = self.program.vertex_list(
                len(vg.triangles) * 3, self.mode,
                batch=self.batch, group=material_group,
                position=('f', position_list),
                texCoords=('f', tex_coords_list),
                normal=('f', normal_list)
            )
            vlists.append(vl)
        return vlists

    def draw(self):
        for vl in self.vertex_lists:
            vl.draw(self.mode)
