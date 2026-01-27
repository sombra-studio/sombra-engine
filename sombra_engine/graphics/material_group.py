from pyglet.graphics import Group, ShaderGroup, ShaderProgram
from pyglet.math import Mat4


from sombra_engine.primitives import Material
from sombra_engine.utils import (
    create_white_tex, create_black_tex, create_gray_tex, create_blue_tex
)


class MaterialGroup(ShaderGroup):
    def __init__(
        self, material: Material, program: ShaderProgram, matrix: Mat4,
        order: int = 0, parent: Group | None = None
    ):
        super().__init__(program, order, parent)
        self.program = program
        self.material = material
        self.matrix = matrix

        # Set ambient map
        self.ambient_map = material.ambient_map
        if self.ambient_map is None:
            self.ambient_map = create_white_tex()
        self.set_texture(self.ambient_map, 0)

        # Set diffuse map
        self.diffuse_map = material.diffuse_map
        if self.diffuse_map is None:
            self.diffuse_map = create_gray_tex()
        self.set_texture(self.diffuse_map, 1)


        # Set specular map
        self.specular_map = material.specular_map
        if self.specular_map is None:
            self.specular_map = create_black_tex()
        self.set_texture(self.specular_map, 2)

        # Set bump map
        if self.material.has_bump_map:
            self.bump_map = material.bump_map
            if self.bump_map is None:
                self.bump_map = create_black_tex()
            self.set_texture(self.bump_map, 3)
        elif self.material.has_normal_map:
            self.normal_map = material.normal_map
            if self.normal_map is None:
                self.normal_map = create_blue_tex()
            self.set_texture(self.normal_map, 3)

        # Uniforms from material
        uniforms = {}
        if 'material.ambient' in self.program._uniforms:
            uniforms['material.ambient'] = self.material.ambient

        if 'material.diffuse' in self.program._uniforms:
            uniforms['material.diffuse'] = self.material.diffuse

        if 'material.specular' in self.program._uniforms:
            uniforms['material.specular'] = self.material.specular

        if 'material.specular_exponent' in self.program._uniforms:
            uniforms['material.specular_exponent'] = \
                self.material.specular_exponent

        if 'material.bump_scale' in self.program._uniforms:
            uniforms['material.bump_scale'] = self.material.bump_scale

        if 'material.has_bump_map' in self.program._uniforms:
            uniforms['material.has_bump_map'] = self.material.has_bump_map

        if 'material.has_normal_map' in self.program._uniforms:
            uniforms['material.has_normal_map'] = \
                self.material.has_normal_map

        if 'material.has_specular_map' in self.program._uniforms:
            uniforms['material.has_specular_map'] = \
                self.material.has_specular_map

        if 'model' in self.program._uniforms:
            uniforms['model'] = self.matrix

        self.set_shader_uniforms(program, uniforms)

