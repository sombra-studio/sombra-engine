from pyglet.math import Vec3


class Transform:
    def __init__(
        self,
        translation: Vec3 = Vec3(),
        rotation: Vec3 = Vec3(),
        scale: Vec3 = Vec3()
    ):
        self.translation = translation
        self.rotation = rotation
        self.scale = scale
