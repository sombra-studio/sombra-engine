from pyglet.graphics import Group
from pyglet.graphics.shader import ShaderProgram
from pyglet.math import Mat4


from sombra_engine.graphics import MaterialGroup
from sombra_engine.primitives import Material


MAX_BONES = 100


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
        self.bones_transforms = []
        for i in range(MAX_BONES):
            self.bones_transforms.append(Mat4())


    def set_state(self):
        super().set_state()
        self.program['bones_transforms'] = self.bones_transforms
