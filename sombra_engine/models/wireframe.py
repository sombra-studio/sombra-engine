from importlib.resources import files
import pyglet
from pyglet.gl import *
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.graphics.vertexdomain import VertexList
from pyglet.math import Vec4


from sombra_engine.graphics import WireframeGroup
from sombra_engine.models import Mesh


class Wireframe:
    def __init__(
        self,
        mesh: Mesh,
        vertex_shader: Shader = None,
        batch: Batch = None,
        group: Group = None,
        color: Vec4 = Vec4(1.0, 1.0, 1.0, 1.0)
    ):
        self.mesh = mesh
        if not vertex_shader:
            vs_src = files('sombra_engine.shaders').joinpath(
                'default.vert'
            ).read_text()
            vertex_shader = Shader(vs_src, 'vertex')
        self.vertex_shader = vertex_shader
        self.batch = batch or pyglet.graphics.get_default_batch()
        self.group = group
        fs_src = files('sombra_engine.shaders').joinpath(
            'wireframe.frag'
        ).read_text()
        fragment_shader = Shader(fs_src, 'fragment')
        self.program = ShaderProgram(vertex_shader, fragment_shader)
        self.program['color'] = color
        self.vertex_lists = self.create_vertex_lists()

    def create_vertex_lists(self) -> list[VertexList]:
        """
        This method creates a vertex list for each vertex group and returns all
        of them in a list.

        Returns:
            list[VertexList]: The list with the newly created vertex lists.
        """
        vlists = []
        # Create a list for position
        group = WireframeGroup(self.program, parent=self.group)
        for vg in self.mesh.vertex_groups.values():
            position_list = []
            for triangle in vg.triangles:
                # Only render
                for v in triangle.vertices:
                    position_list += [v.position.x, v.position.y, v.position.z]
            vl = self.program.vertex_list(
                len(vg.triangles) * 3, GL_TRIANGLES,
                batch=self.batch, group=group,
                position=('f', position_list)
            )
            vlists.append(vl)
        return vlists

    def draw(self):
        for vl in self.vertex_lists:
            vl.draw(GL_TRIANGLES)
