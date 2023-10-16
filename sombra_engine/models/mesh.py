from pyglet.gl import *
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram
from pyglet.graphics.vertexdomain import VertexDomain

from sombra_engine.graphics import MaterialGroup
from sombra_engine.primitives import *


class Mesh:
    def __init__(
        self,
        name: str,
        vertices: list[Vertex],
        indices: list[int],
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
        self.vertices = vertices
        self.indices = indices
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

    def create_vertex_lists(self) -> list[VertexDomain]:
        """
        This method creates a vertex list for each vertex group using the
        Shader Program that this Mesh currently has, and returns all
        of them in a list.

        Returns:
            list[VertexDomain]: The list with the newly created vertex lists.
        """
        vlists = []
        # Create a list for position
        position_list = self.get_positions_array()
        # Create a list for texCoords
        texcoords_list = self.get_tex_coords_array()
        # Create a list for normal
        normal_list = self.get_normals_array()

        for vg in self.vertex_groups.values():
            material_group = self.material_groups[vg.material.name]
            vl = self.program.vertex_list_indexed(
                len(vg.indices), self.mode, vg.indices,
                batch=self.batch, group=material_group,
                position=('f', position_list),
                texCoords=('f', texcoords_list),
                normal=('f', normal_list)
            )
            vlists.append(vl)
        return vlists

    def draw(self):
        for vl in self.vertex_lists:
            vl.draw(self.mode)

    def get_vertex_attr_array(self, attrib_name):
        answer = []
        for v in self.vertices:
            attrib = getattr(v, attrib_name)
            if isinstance(attrib, Vec3):
                answer += [attrib.x, attrib.y, attrib.z]
            elif isinstance(attrib, Vec2):
                answer += [attrib.x, attrib.y]
            else:
                raise Exception(
                    f"invalid type {type(attrib)} for vertex attribute "
                    f"{attrib_name}"
                )
        return answer

    def get_positions_array(self):
        answer = self.get_vertex_attr_array('position')
        return answer

    def get_normals_array(self):
        answer = self.get_vertex_attr_array('normal')
        return answer

    def get_tex_coords_array(self):
        answer = self.get_vertex_attr_array('tex_coords')
        return answer
