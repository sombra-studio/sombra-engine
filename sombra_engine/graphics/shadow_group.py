from pyglet.graphics import ShaderGroup, ShaderProgram, Texture
from pyglet.math import Mat4
from typing import Any


class ShadowGroup(ShaderGroup):
    def __init__(
        self,
        light_transform: Mat4,
        shadow_map: Texture,
        program: ShaderProgram,
        matrix: Mat4 = Mat4()
    ):
        super().__init__(program)
        self.light_transform = light_transform
        self.program = program
        self.matrix = matrix
        self.uniforms = self.get_uniforms()
        self.set_shader_uniforms(program, self.uniforms)
        self.set_texture(shadow_map)

    def get_uniforms(self) -> dict[str, Any]:
        uniforms = {}
        uniforms['light_transform'] = self.light_transform
        uniforms['model'] = self.matrix
        return uniforms