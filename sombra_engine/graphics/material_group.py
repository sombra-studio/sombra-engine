from pyglet.gl import *
from pyglet.graphics import Group
from pyglet.graphics.shader import ShaderProgram
from pyglet.math import Mat4
import pyglet.resource

from sombra_engine.primitives import Material
from sombra_engine import utils


class MaterialGroup(Group):
    def __init__(
        self, material: Material, program: ShaderProgram, matrix: Mat4,
        order: int = 0, parent: Group = None
    ):
        super().__init__(order, parent)
        self.program = program
        self.material = material
        self.matrix = matrix

        # Set diffuse map
        if material.diffuse_map:
            self.diffuse_map = pyglet.resource.image(material.diffuse_map)
        else:
            self.diffuse_map = utils.create_white_tex()

        # Set ambient map
        if material.ambient_map:
            self.ambient_map = pyglet.resource.image(material.ambient_map)
        else:
            self.ambient_map = utils.create_white_tex()

        # Set specular map
        if material.specular_map:
            self.specular_map = pyglet.resource.image(material.specular_map)
        else:
            self.specular_map = utils.create_black_tex()

    def set_state(self):
        self.program.use()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(self.ambient_map.target, self.ambient_map.id)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(self.diffuse_map.target, self.diffuse_map.id)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(self.specular_map.target, self.specular_map.id)
        self.program['material.ambient'] = self.material.ambient
        self.program['material.diffuse'] = self.material.diffuse
        self.program['material.specular'] = self.material.specular
        self.program['material.specular_exponent'] = \
            self.material.specular_exponent
        self.program['model'] = self.matrix

    def unset_state(self):
        self.program.stop()

    def __hash__(self):
        return hash(
            (self.material, self.program, self.order, self.parent)
        )

    def __eq__(self, other):
        return (
            isinstance(other, MaterialGroup) and
            self.material == other.material and
            self.program == other.program and
            self.order == other.order and
            self.parent == other.parent
        )
