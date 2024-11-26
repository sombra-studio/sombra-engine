import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram

class Gizmo:
    def __init__(self, size:float = 1.0):
        vs = Shader("shaders/gizmo.vert", 'vertex')
        fs = Shader("shaders/gizmo.frag", 'fragment')
        program = ShaderProgram(vs, fs)
        self.mode = pyglet.gl.GL_LINES
        self.vertex_list = program.vertex_list(
            6, self.mode,
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
