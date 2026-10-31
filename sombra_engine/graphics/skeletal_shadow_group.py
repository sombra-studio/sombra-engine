from pyglet.graphics import ShaderProgram
from pyglet.math import Mat4, Vec3
from typing import Any


from sombra_engine.constants import MAX_BONES
from sombra_engine.graphics.shadow_group import ShadowGroup


class SkeletalShadowGroup(ShadowGroup):
    def __init__(
        self,
        light_transform: Mat4,
        program: ShaderProgram,
        matrix: Mat4 = Mat4()
    ):
        self.bones_transforms = []
        for i in range(MAX_BONES):
            mat = Mat4.from_translation(Vec3(1.0, 0.0, 0.0))
            self.bones_transforms.append(mat)

        super().__init__(
            light_transform=light_transform,
            program=program,
            matrix=matrix
        )

    def create_uniforms(self) -> dict[str, Any]:
        uniforms = super().create_uniforms()
        uniforms['bones_transforms'] = self.bones_transforms
        return uniforms

