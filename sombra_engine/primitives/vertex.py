from pyglet.math import Vec2, Vec3


class Vertex:
    def __init__(
        self,
        vertex_id: int,
        position: Vec3 = Vec3(),
        normal: Vec3 = Vec3(0.0, 1.0, 0.0),
        tex_coords: Vec2 = Vec2()
    ):
        self.vertex_id = vertex_id
        self.position = position
        self.normal = normal
        self.tex_coords = tex_coords

    def get_attr_tuple(self, name: str) -> tuple[float, float, float]:
        vec: Vec3 = getattr(self, name)
        return vec.x, vec.y, vec.z
