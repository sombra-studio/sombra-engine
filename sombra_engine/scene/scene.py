from pyglet.math import Vec3


from sombra_engine.models import Mesh
from sombra_engine.scene import Light


class Scene:
    def __init__(self):
        self.lights: list[Light] = []
        self.meshes: list[Mesh] = []

    def create_light(self, position: Vec3, color: Vec3):
        light = Light(position, color)
        self.lights.append(light)

    def remove_light(self, idx: int):
        self.lights.pop(idx)

    def add_mesh(self, mesh: Mesh):
        # change the group of each mesh so that includes the light
        self.meshes.append(mesh)
