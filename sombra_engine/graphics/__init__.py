import pyglet
from pyglet.gl import *
from pyglet.graphics import ShaderGroup, Group


from sombra_engine.primitives import Material


class MaterialGroup(ShaderGroup):
    def __init__(
        self, material: Material, program: pyglet.graphics.shader.ShaderProgram,
        order: int = 0, parent: Group = None
    ):
        super().__init__(program, order, parent)
        self.material = material


    def set_state(self):
        material = self.program.uniform_blocks['Material'].create_ubo()
        material.ambient = self.material.ambient
        material.diffuse = self.material.diffuse
        material.specular = self.material.specular

