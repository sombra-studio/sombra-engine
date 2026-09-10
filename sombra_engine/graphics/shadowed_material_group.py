from pyglet.graphics import Group, ShaderProgram
from pyglet.math import Mat4
from typing import Any


from sombra_engine.graphics import MaterialGroup
from sombra_engine.primitives import Material


class ShadowedMaterialGroup(MaterialGroup):
    def __init__(
        self,
        material: Material,
        program: ShaderProgram,
        matrix: Mat4 = Mat4(),
        light_transform: Mat4 = Mat4(),
        order: int = 0,
        parent: Group | None = None
    ):
        self.light_transform = light_transform
        super().__init__(
            material=material,
            program=program,
            matrix=matrix,
            order=order,
            parent=parent
        )
        # TODO add shadow map texture

    def get_uniforms(self) -> dict[str, Any]:
        uniforms = super().get_uniforms()
        uniforms['light_transform'] = self.light_transform
        return uniforms
