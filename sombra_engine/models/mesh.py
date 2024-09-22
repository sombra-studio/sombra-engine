from pyglet.gl import *
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram
from pyglet.graphics.vertexdomain import VertexList
from pyglet.math import Vec3

from sombra_engine.graphics import MaterialGroup
from sombra_engine.primitives import (
    Material, SceneObject, Transform, VertexGroup
)


class Mesh(SceneObject):
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
        super().__init__(transform)
        self.name = name
        self.vertex_groups = vertex_groups
        self.materials = materials
        self.mode = mode
        self.batch = batch or pyglet.graphics.get_default_batch()
        self.group = group
        self.program = program or pyglet.graphics.get_default_shader()
        self.parent = parent

        self.material_groups = self.create_material_groups()
        self.vertex_lists = self.create_vertex_lists()

    # Create methods
    # -------------------------------------------------------------------------
    def create_material_groups(self) -> dict[str, MaterialGroup]:
        groups = {}
        for name, material in self.materials.items():
            new_group = MaterialGroup(
                material, self.program, self.get_matrix(),
                order=0, parent=self.group
            )
            groups[name] = new_group
        return groups

    def create_vertex_lists(self) -> list[VertexList]:
        """
        This method creates a vertex list for each vertex group using the
        Shader Program that this Mesh currently has, and returns all
        of them in a list.

        Returns:
            list[VertexList]: The list with the newly created vertex
                lists.
        """
        vlists = []

        for vg_name, vg in self.vertex_groups.items():
            (
                position_list, tex_coords_list, normal_list
            ) = self.get_lists_for_vertex_group(vg_name)
            material_group = self.material_groups[vg.material.name]
            vl = self.program.vertex_list(
                len(vg.triangles) * 3, self.mode,
                batch=self.batch, group=material_group,
                position=('f', position_list),
                tex_coords=('f', tex_coords_list),
                normal=('f', normal_list)
            )
            vlists.append(vl)
        return vlists

    # Transform methods
    # -------------------------------------------------------------------------
    def update_matrix(self):
        matrix = self.get_matrix()
        for material_group in self.material_groups.values():
            material_group.matrix = matrix

    def rotate_x(self, angle: float):
        rot = self.transform.rotation
        self.transform.rotation = Vec3(angle, rot.y, rot.z)
        self.update_matrix()

    def rotate_y(self, angle: float):
        self.transform.rotation.y = angle
        self.update_matrix()

    def rotate_z(self, angle: float):
        self.transform.rotation.z = angle
        self.update_matrix()

    def translate(self, vec: Vec3):
        self.transform.translation = vec
        self.update_matrix()

    def scale(self, vec: Vec3):
        self.transform.scale = vec
        self.update_matrix()

    # -------------------------------------------------------------------------

    def draw(self):
        for vl in self.vertex_lists:
            vl.draw(self.mode)

    def get_lists_for_vertex_group(self, vertex_group_name: str) -> tuple[
        list[float], list[float], list[float]
    ]:
        if vertex_group_name not in self.vertex_groups:
            raise KeyError(
                f"Couldn't find key {vertex_group_name} for vertex group in "
                f"mesh {self.name}"
            )
        position_list = []
        tex_coords_list = []
        normal_list = []
        for triangle in self.vertex_groups[vertex_group_name].triangles:
            for v in triangle.vertices:
                position_list += [v.position.x, v.position.y, v.position.z]
                tex_coords_list += [v.tex_coords.x, v.tex_coords.y]
                normal_list += [v.normal.x, v.normal.y, v.normal.z]
        return position_list, tex_coords_list, normal_list
