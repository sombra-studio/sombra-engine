from pyglet.gl import *
from pyglet.graphics import ShaderGroup, Group
import pyglet.resource

from sombra_engine.primitives import Material
from sombra_engine import utils


class MaterialGroup(ShaderGroup):
    def __init__(
        self, material: Material, program: pyglet.graphics.shader.ShaderProgram,
        order: int = 0, parent: Group = None
    ):
        super().__init__(program, order, parent)
        # Set ambient
        self.ambient = material.ambient
        if material.ambient_map:
            self.ambient_map = pyglet.resource.image(material.ambient_map)
        else:
            self.ambient_map = utils.create_white_tex()

        # Set diffuse
        self.diffuse = material.diffuse
        if material.diffuse_map:
            self.diffuse_map = pyglet.resource.image(material.diffuse_map)
        else:
            self.diffuse_map = utils.create_white_tex()

        # Set specular
        self.specular = material.specular
        if material.specular_map:
            self.specular_map = pyglet.resource.image(material.specular_map)
        else:
            self.specular_map = utils.create_black_tex()

        # Set specular exponent
        self.specular_exponent = material.specular_exponent


    def set_state(self):
        glEnable(GL_DEPTH_TEST)
        material_ubo = self.program.uniform_blocks['Material'].create_ubo()
        with material_ubo as material:
            material.ambient = self.ambient
            material.diffuse = self.diffuse
            material.specular = self.specular
            material.specular_exponent = self.specular_exponent
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(self.ambient_map.target, self.ambient_map.id)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(self.diffuse_map.target, self.diffuse_map.id)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(self.specular_map.target, self.specular_map.id)
