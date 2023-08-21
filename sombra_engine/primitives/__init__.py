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


class Material:
    def __init__(
        self,
        material_id: int,
        name: str = "default",
        ambient: Vec3 = Vec3(1.0),
        diffuse: Vec3 = Vec3(1.0),
        specular: Vec3 = Vec3(1.0),
        specular_exponent: int = 0,
        ior: float = 1.0,
        ambient_map: str = "",
        diffuse_map: str = "",
        specular_map: str = ""
    ):
        self.material_id = material_id
        self.name = name
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.specular_exponent = specular_exponent
        self.ior = ior
        self.ambient_map = ambient_map
        self.diffuse_map = diffuse_map
        self.specular_map = specular_map


class Triangle:
    def __init__(self, a: Vertex, b: Vertex, c: Vertex):
        self.a = a
        self.b = b
        self.c = c


class VertexGroup:
    def __init__(self, name: str, indices: list[int], material: Material):
        self.name = name
        self.indices = indices
        self.material = material


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
