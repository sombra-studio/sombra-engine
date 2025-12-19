from pyglet.gl import *
from pyglet.graphics import Group
from pyglet.graphics.shader import ShaderProgram
from pyglet.math import Mat4


from sombra_engine.primitives import Material


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
        self.diffuse_map = material.diffuse_map
        glBindTexture(self.diffuse_map.target, self.diffuse_map.id)
        glGenerateMipmap(self.diffuse_map.target)

        # Set ambient map
        self.ambient_map = material.ambient_map
        glBindTexture(self.ambient_map.target, self.ambient_map.id)
        glGenerateMipmap(self.ambient_map.target)

        # Set specular map
        self.specular_map = material.specular_map
        glBindTexture(self.specular_map.target, self.specular_map.id)
        glGenerateMipmap(self.specular_map.target)

        # Set bump map
        if self.material.has_bump_map:
            self.bump_map = material.bump_map
            glBindTexture(self.bump_map.target, self.bump_map.id)
            glGenerateMipmap(self.bump_map.target)
        elif self.material.has_normal_map:
            self.normal_map = material.normal_map
            glBindTexture(self.normal_map.target, self.normal_map.id)
            glGenerateMipmap(self.normal_map.target)

    def set_state(self):
        self.program.use()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(self.ambient_map.target, self.ambient_map.id)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(self.diffuse_map.target, self.diffuse_map.id)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(self.specular_map.target, self.specular_map.id)
        glActiveTexture(GL_TEXTURE3)
        if self.material.has_bump_map:
            glBindTexture(self.bump_map.target, self.bump_map.id)
        elif self.material.has_normal_map:
            glBindTexture(self.normal_map.target, self.normal_map.id)
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

        if 'material.has_normal_map' in self.program._uniforms:
            self.program['material.has_normal_map'] = \
                self.material.has_normal_map

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
