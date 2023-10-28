from pyglet.gl import *
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.graphics.vertexdomain import VertexDomain
from pyglet.math import Vec3

from sombra_engine.models import Mesh


class WireframeGroup(Group):
    def __init__(self, program: ShaderProgram, order: int = 30, parent=None):
        super().__init__(order=order, parent=parent)
        self.program = program

    def set_state(self):
        self.program.use()
        pyglet.gl.glPolygonMode(pyglet.gl.GL_FRONT_AND_BACK, pyglet.gl.GL_LINE)

    def unset_state(self):
        self.program.stop()
        pyglet.gl.glPolygonMode(pyglet.gl.GL_FRONT_AND_BACK, pyglet.gl.GL_FILL)


class Wireframe:
    def __init__(
        self,
        mesh: Mesh,
        vertex_shader: Shader,
        batch: Batch = pyglet.graphics.get_default_batch(),
        group: Group = None,
        color: Vec3 = Vec3(1.0, 1.0, 1.0)
    ):
        self.mesh = mesh
        self.vertex_shader = vertex_shader
        self.batch = batch or pyglet.graphics.get_default_batch()
        self.group = group
        with open('sombra_engine/shaders/solid.frag') as f:
            fragment_shader = Shader(f.read(), 'fragment')
        self.program = ShaderProgram(vertex_shader, fragment_shader)
        self.program.uniforms['material.diffuse'].set(color)
        self.vertex_lists = self.create_vertex_lists()

    def create_vertex_lists(self) -> list[VertexDomain]:
        """
        This method creates a vertex list for each vertex group and returns all
        of them in a list.

        Returns:
            list[VertexDomain]: The list with the newly created vertex lists.
        """
        vlists = []
        # Create a list for position
        position_list = self.mesh.get_positions_array()
        group = WireframeGroup(self.program, parent=self.group)
        for vg in self.mesh.vertex_groups.values():
            vl = self.program.vertex_list_indexed(
                len(vg.indices), GL_TRIANGLES, vg.indices,
                batch=self.batch, group=group,
                position=('f', position_list)
            )
            vlists.append(vl)
        return vlists

    def draw(self):
        for vl in self.vertex_lists:
            vl.draw(GL_TRIANGLES)
