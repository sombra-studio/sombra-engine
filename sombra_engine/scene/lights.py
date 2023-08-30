from pyglet.math import Vec3


class Light:
    def __init__(self, position: Vec3, color: Vec3):
        self.position = position
        self.color = color
