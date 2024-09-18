from pyglet.gl import *
from pyglet.graphics import Group
from pyglet.graphics.shader import ShaderProgram


class WireframeGroup(Group):
    def __init__(self, program: ShaderProgram, order: int = 30, parent=None):
        super().__init__(order=order, parent=parent)
        self.program = program

    def set_state(self):
        self.program.use()
        glEnable(GL_POLYGON_OFFSET_LINE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glPolygonOffset(0.0, -0.001)

    def unset_state(self):
        self.program.stop()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDisable(GL_POLYGON_OFFSET_LINE)
        # glPolygonOffset(0.0, 0.0)
