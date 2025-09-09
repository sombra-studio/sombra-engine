from pyglet.math import Vec2, Vec3, Vec4


class Vertex:
    def __init__(
        self,
        position: Vec3 = Vec3(),
        normal: Vec3 = Vec3(0.0, 1.0, 0.0),
        tangent: Vec3 = Vec3(),
        tex_coords: Vec2 = Vec2(),
        bones_ids: tuple[int, int, int, int] = (0, 0, 0, 0),
        weights: Vec4 = Vec4(1.0)
    ):
        self.position = position
        self.normal = normal
        self.tangent = tangent
        self.tex_coords = tex_coords
        self.bones_ids = bones_ids
        self.weights = weights
