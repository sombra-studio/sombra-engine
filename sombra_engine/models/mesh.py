from importlib.resources import files
from pyglet.gl import *
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.graphics.vertexdomain import VertexList
from pyglet.math import Vec2, Vec3
import pyglet

from sombra_engine.graphics import MaterialGroup
from sombra_engine.primitives import (
    Material, SceneObject, Transform, Vertex, VertexGroup
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
        if not program:
            vs_src = files('sombra_engine.shaders').joinpath(
                'default.vert'
            ).read_text()
            vert_shader = Shader(vs_src, 'vertex')

            fs_src = files('sombra_engine.shaders').joinpath(
                'blinn_barycentric.frag'
            ).read_text()
            frag_shader = Shader(fs_src, 'fragment')

            program = ShaderProgram(vert_shader, frag_shader)
        self.program = program
        self.parent = parent

        self.material_groups = self.create_material_groups()
        self.vertex_lists = self.create_vertex_lists()
        self.tri_count: int = 0
        self.calculate_tri_count(vertex_groups)

    @staticmethod
    def check_tex_coords(a: Vertex, b: Vertex, c: Vertex):
        empty: Vec2 = Vec2()
        if (
            a.tex_coords == empty and
            b.tex_coords == empty and
            c.tex_coords == empty
        ):
            # Assign arbitrary texture coordinates when not defined
            a.tex_coords = Vec2(0.0, 1.0)
            b.tex_coords = Vec2(0.0, 0.0)
            c.tex_coords = Vec2(1.0, 0.0)

    def calculate_normals(self):
        """
        Calculate normal and tangent vectors for every vertex.
        Also define texture coordinates if they are not defined.
        """
        for vertex_group in self.vertex_groups.values():
            for triangle in vertex_group.triangles:
                a = triangle.vertices[0]
                b = triangle.vertices[1]
                c = triangle.vertices[2]
                self.check_tex_coords(a, b, c)
                # Formulas from:
                #   https://learnopengl.com/Advanced-Lighting/Normal-Mapping
                edge_1: Vec3 = b.position - a.position
                edge_2: Vec3 = c.position - a.position
                delta_uv1: Vec2 = b.tex_coords - a.tex_coords
                delta_uv2: Vec2 = c.tex_coords - a.tex_coords
                inverse_scalar = (
                    delta_uv1.x * delta_uv2.y - delta_uv2.x * delta_uv1.y
                )
                if inverse_scalar == 0:
                    continue
                f: float = 1.0 / inverse_scalar

                tangent_x: float = f * (
                    delta_uv2.y * edge_1.x - delta_uv1.y * edge_2.x
                )
                tangent_y: float = f * (
                    delta_uv2.y * edge_1.y - delta_uv1.y * edge_2.y
                )
                tangent_z: float = f * (
                    delta_uv2.y * edge_1.z - delta_uv1.y * edge_2.z
                )
                tangent = Vec3(tangent_x, tangent_y, tangent_z).normalize()

                a.tangent = tangent
                b.tangent = tangent
                c.tangent = tangent

    def calculate_tri_count(self, vertex_groups: dict[str, VertexGroup]):
        self.tri_count: int = 0
        for vg_name, vg in vertex_groups.items():
            self.tri_count += len(vg.triangles)

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
        # first calculate normals
        self.calculate_normals()

        vlists = []

        for vg_name, vg in self.vertex_groups.items():
            (
                position_list, normal_list, tangent_list, tex_coords_list
            ) = self.get_lists_for_vertex_group(vg_name)
            material_group = self.material_groups[vg.material.name]
            vl = self.program.vertex_list(
                len(vg.triangles) * 3, self.mode,
                batch=self.batch, group=material_group,
                position=('f', position_list),
                normal=('f', normal_list),
                tangent=('f', tangent_list),
                tex_coords=('f', tex_coords_list)

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
        self.transform.rotation += Vec3(angle, 0.0, 0.0)
        self.update_matrix()

    def rotate_y(self, angle: float):
        self.transform.rotation += Vec3(0.0, angle, 0.0)
        self.update_matrix()

    def rotate_z(self, angle: float):
        self.transform.rotation += Vec3(0.0, 0.0, angle)
        self.update_matrix()

    def translate(self, vec: Vec3):
        self.transform.translation += vec
        self.update_matrix()

    def scale(self, vec: Vec3):
        self.transform.scale *= vec
        self.update_matrix()

    # -------------------------------------------------------------------------

    def draw(self):
        for vl in self.vertex_lists:
            vl.draw(self.mode)

    def get_lists_for_vertex_group(self, vertex_group_name: str) -> tuple[
        list[float], list[float], list[float], list[float]
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
        for triangle in self.vertex_groups[vertex_group_name].triangles:
            for v in triangle.vertices:
                position_list += [v.position.x, v.position.y, v.position.z]
                normal_list += [v.normal.x, v.normal.y, v.normal.z]
                tangent_list += [v.tangent.x, v.tangent.y, v.tangent.z]
                tex_coords_list += [v.tex_coords.x, v.tex_coords.y]
        return position_list, normal_list, tangent_list, tex_coords_list

    def update(self, dt):
        pass
