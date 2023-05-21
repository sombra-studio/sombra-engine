import pyglet
from pyglet.math import Vec2, Vec3


class Vertex:
    def __init__(
        self,
        position: Vec3 = Vec3(),
        color: Vec3 = Vec3(),
        normal: Vec3 = Vec3(),
        tex_coords: Vec2 = Vec2()
    ):
        self.position = position
        self.color = color
        self.normal = normal
        self.tex_coords = tex_coords


class Transform:
    def __init__(
        self,
        position: Vec3 = Vec3(),
        rotation: Vec3 = Vec3(),
        scale: Vec3 = Vec3()
    ):
        self.position = position
        self.rotation = rotation
        self.scale = scale
