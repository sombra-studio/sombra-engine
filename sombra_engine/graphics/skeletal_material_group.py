from pyglet.graphics import Group, ShaderProgram
from pyglet.math import Mat4


from sombra_engine.graphics import MaterialGroup
from sombra_engine.primitives import Material


class SkeletalMaterialGroup(MaterialGroup):
    def __init__(
        self, material: Material, program: ShaderProgram, matrix: Mat4,
        order: int = 0, parent: Group = None
    ):
        super().__init__(
            material=material,
            program=program,
            matrix=matrix,
            order=order,
            parent=parent
        )

    def set_state(self):
        super().set_state()
        self.program['bones_transforms'] = [
            Mat4() for _ in range(100)
        ]
