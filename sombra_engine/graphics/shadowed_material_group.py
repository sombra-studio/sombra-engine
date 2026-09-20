from pyglet.graphics import Group, ShaderProgram, Texture
from pyglet.math import Mat4
from typing import Any


from sombra_engine.graphics import MaterialGroup
from sombra_engine.primitives import Material


class ShadowedMaterialGroup(MaterialGroup):
    def __init__(
        self,
        material: Material,
        program: ShaderProgram,
        depth_map: Texture,
        matrix: Mat4 = Mat4(),
        light_transform: Mat4 = Mat4(),
        order: int = 0,
        parent: Group | None = None
    ):
        self.depth_map = depth_map
        self.light_transform = light_transform
        super().__init__(
            material=material,
            program=program,
            matrix=matrix,
            order=order,
            parent=parent
        )

    def create_textures(self) -> dict[str, Texture]:
        textures = super().create_textures()
        textures['depth_map'] = self.depth_map
        return textures

    def create_uniforms(self) -> dict[str, Any]:
        uniforms = super().create_uniforms()
        uniforms['light_transform'] = self.light_transform
        return uniforms
