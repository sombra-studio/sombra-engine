from pyglet.math import Mat4, Vec3


class Transform:
    def __init__(
        self,
        translation: Vec3 = Vec3(),
        rotation: Vec3 = Vec3(),
        scale: Vec3 = Vec3(1.0, 1.0, 1.0)
    ):
        self.translation = translation
        self.rotation = rotation
        self.scale = scale

    def get_matrix(self) -> Mat4:
        scale = Mat4.from_scale(self.scale)
        rotation_x = Mat4.from_rotation(self.rotation.x, Vec3(1.0, 0.0, 0.0))
        rotation_y = Mat4.from_rotation(self.rotation.x, Vec3(0.0, 1.0, 0.0))
        rotation_z = Mat4.from_rotation(self.rotation.x, Vec3(0.0, 0.0, 1.0))
        rotation = rotation_x @ rotation_y @ rotation_z
        translation = Mat4.from_translation(self.translation)
        final = scale @ translation @ rotation
        return final
