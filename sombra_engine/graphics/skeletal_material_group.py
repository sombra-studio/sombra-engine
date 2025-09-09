from pyglet.graphics import Group
from pyglet.graphics.shader import ShaderProgram
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
        transforms_list = []
        for i in range(100):
            # transforms_list += (
            #     1, 0, 0, 0,
            #     0, 1, 0, 0,
            #     0, 0, 1, 0,
            #     0, 0, 0, 1
            # )
            transforms_list.append(Mat4())
        self.program['bones_transforms'] = transforms_list
