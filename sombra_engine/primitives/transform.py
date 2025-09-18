from pyglet.math import Mat4, Vec3


from sombra_engine.utils import Quaternion


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

    def get_rotation_as_mat4(self) -> Mat4:
        rotation_x = Mat4.from_rotation(self.rotation.x, Vec3(1.0, 0.0, 0.0))
        rotation_y = Mat4.from_rotation(self.rotation.y, Vec3(0.0, 1.0, 0.0))
        rotation_z = Mat4.from_rotation(self.rotation.z, Vec3(0.0, 0.0, 1.0))
        rotation = rotation_x @ rotation_y @ rotation_z
        return rotation

    def get_matrix(self) -> Mat4:
        scale = Mat4.from_scale(self.scale)
        rotation = self.get_rotation_as_mat4()
        translation = Mat4.from_translation(self.translation)
        final = scale @ translation @ rotation
        return final

    @staticmethod
    def interpolate(a: 'Transform', b: 'Transform', t: float) -> Mat4:
        new_translation = a.translation.lerp(b.translation, t)

        # Rotation
        q_a = Quaternion.from_mat4(a.get_rotation_as_mat4())
        q_b = Quaternion.from_mat4(b.get_rotation_as_mat4())
        q_interpolated = q_a @ q_b
        rotation = q_interpolated.to_mat4()

        new_scale = a.scale.lerp(b.scale, t)

        scale = Mat4.from_scale(new_scale)
        translation = Mat4.from_translation(new_translation)
        final = scale @ translation @ rotation
        return final
