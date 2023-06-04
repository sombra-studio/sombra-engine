import pyglet
from pyglet.math import Vec2, Vec3


class Vertex:
    def __init__(
        self,
        id: int,
        position: Vec3 = Vec3(),
        color: Vec3 = Vec3(1.0),
        normal: Vec3 = Vec3(0.0, 1.0, 0.0),
        tex_coords: Vec2 = Vec2()
    ):
        self.id = id
        self.position = position
        self.color = color
        self.normal = normal
        self.tex_coords = tex_coords


class Material:
    def __init__(
        self,
        id: int,
        name: str = "default",
        ambient: Vec3 = Vec3(1.0),
        diffuse: Vec3 = Vec3(1.0),
        specular: Vec3 = Vec3(1.0),
        specular_exponent: int = 0,
        roughness: float = 1.0,
        ior: float = 1.0
    ):
        self.id = id
        self.name = name
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.specular_exponent = specular_exponent
        self.roughness = roughness
        self.ior = ior
        self.ambient_map = None
        self.diffuse_map = None
        self.specular_map = None
        self.roughness_map = None


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
