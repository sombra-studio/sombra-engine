import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram


class Gizmo:
    def __init__(
        self,
        size:float = 1.0,
        batch:pyglet.graphics.Batch = None,
        group:pyglet.graphics.Group = None
    ):
        with open("sombra_engine/shaders/gizmo.vert") as f:
            vs = Shader(f.read(), 'vertex')
        with open("sombra_engine/shaders/gizmo.frag") as f:
            fs = Shader(f.read(), 'fragment')
        self.program = ShaderProgram(vs, fs)
        self.mode = pyglet.gl.GL_LINES
        self.vertex_list = self.program.vertex_list(
            6, self.mode, batch=batch, group=group,
            position=(
                'f', (
                    0.0, 0.0, 0.0,  size, 0.0, 0.0,
                    0.0, 0.0, 0.0,  0.0, size, 0.0,
                    0.0, 0.0, 0.0,  0.0, 0.0, size
                )
            ),
            color=(
                'Bn', (
                    200, 0, 0,  200, 0, 0,
                    0, 200, 0,  0, 200, 0,
                    0, 0, 200,  0, 0, 200
                )
            )
        )

    def draw(self):
        self.vertex_list.draw(self.mode)
