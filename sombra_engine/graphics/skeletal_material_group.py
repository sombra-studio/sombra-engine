from pyglet.graphics import Group, ShaderProgram
from pyglet.math import Mat4, Vec3
from typing import Any


from sombra_engine.constants import MAX_BONES
from sombra_engine.graphics import MaterialGroup
from sombra_engine.primitives import Material


class SkeletalMaterialGroup(MaterialGroup):
    def __init__(
        self,
        material: Material,
        program: ShaderProgram,
        matrix: Mat4 = Mat4(),
        order: int = 0,
        parent: Group | None = None
    ):
        self.bones_transforms = []
        for i in range(MAX_BONES):
            mat = Mat4.from_translation(Vec3(1.0, 0.0, 0.0))
            self.bones_transforms.append(mat)

        super().__init__(
            material=material,
            program=program,
            matrix=matrix,
            order=order,
            parent=parent
        )

    def get_uniforms(self) -> dict[str, Any]:
        uniforms = super().get_uniforms()
        uniforms['bones_transforms'] = self.bones_transforms
        return uniforms
