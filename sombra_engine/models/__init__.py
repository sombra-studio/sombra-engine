from pyglet.gl import *
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram


from sombra_engine.primitives import *


class SceneObject:
    def __init__(self, transform: Transform = Transform()):
        self.transform = transform


class Mesh:
    def __init__(
        self,
        name: str,
        vertices: list[Vertex],
        indices: list[int],
        vertex_groups: list[VertexGroup] = None,
        materials: list[Material] = None,
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

        self.vertex_list = self.create_vertex_list()

    def create_vertex_list(self):
        vao = self.program.vertex_list_indexed(
            len(self.indices), self.mode, self.batch, self.group,
            position=('f', self.get_vertices_array())
        )
        return vao

    def get_vertices_array(self):
        answer = []
        for v in self.vertices:
            answer += [v.position.x, v.position.y, v.position.z]
        return answer


class Model:
    def __init__(
        self, name: str, meshes: list[Mesh], transform: Transform = Transform(),
        parent: SceneObject = None
    ):
        self.name = name
        self.meshes = meshes
        self.transform = transform
        self.parent = parent
