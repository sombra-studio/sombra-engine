from importlib.resources import files
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import Shader, ShaderProgram
import pyglet


class Gizmo:
    def __init__(
        self,
        size:float = 1.0,
        batch:Batch = None,
        group:Group = None,
    ):
        vs_src = files('sombra_engine.shaders').joinpath(
            'gizmo.vert'
        ).read_text()
        fs_src = files('sombra_engine.shaders').joinpath(
            'gizmo.frag'
        ).read_text()
        vs = Shader(vs_src, 'vertex')
        fs = Shader(fs_src, 'fragment')
        if not batch:
            batch = pyglet.graphics.get_default_batch()
        self.batch = batch
        self.program = ShaderProgram(vs, fs)
        self.mode = pyglet.gl.GL_LINES
        self.vertex_list = self.program.vertex_list(
            6, self.mode, batch=self.batch, group=group,
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
        self.batch.draw()
