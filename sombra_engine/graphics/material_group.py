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
            img = pyglet.image.load(material.diffuse_map)
            self.diffuse_map = img.get_texture()
        else:
            self.diffuse_map = utils.create_white_tex()
        glBindTexture(self.diffuse_map.target, self.diffuse_map.id)
        glGenerateMipmap(self.diffuse_map.target)

        # Set ambient map
        if material.ambient_map:
            img = pyglet.image.load(material.ambient_map)
            self.ambient_map = img.get_texture()
        else:
            self.ambient_map = utils.create_white_tex()
        glBindTexture(self.ambient_map.target, self.ambient_map.id)
        glGenerateMipmap(self.ambient_map.target)

        # Set specular map
        if material.specular_map:
            img = pyglet.image.load(material.specular_map)
            self.specular_map = img.get_texture()
        else:
            self.specular_map = utils.create_black_tex()
        glBindTexture(self.specular_map.target, self.specular_map.id)
        glGenerateMipmap(self.specular_map.target)

        # Set bump map
        if material.bump_map:
            img = pyglet.image.load(material.bump_map)
            self.bump_map = img.get_texture()
        else:
            self.bump_map = utils.create_black_tex()

    def set_state(self):
        self.program.use()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(self.ambient_map.target, self.ambient_map.id)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(self.diffuse_map.target, self.diffuse_map.id)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(self.specular_map.target, self.specular_map.id)
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(self.bump_map.target, self.bump_map.id)
        if 'material.ambient' in self.program._uniforms:
            self.program['material.ambient'] = self.material.ambient

        if 'material.diffuse' in self.program._uniforms:
            self.program['material.diffuse'] = self.material.diffuse

        if 'material.specular' in self.program._uniforms:
            self.program['material.specular'] = self.material.specular

        if 'material.specular_exponent' in self.program._uniforms:
            self.program['material.specular_exponent'] = \
                self.material.specular_exponent

        if 'material.bump_scale' in self.program._uniforms:
            self.program['material.bump_scale'] = self.material.bump_scale

        if 'material.has_bump_map' in self.program._uniforms:
            self.program['material.has_bump_map'] = self.material.has_bump_map

        if 'material.has_specular_map' in self.program._uniforms:
            self.program['material.has_specular_map'] = \
                self.material.has_specular_map

        if 'model' in self.program._uniforms:
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
