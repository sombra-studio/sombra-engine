from pyglet.math import Vec3


from sombra_engine.models import Mesh

class Light:
    def __init__(self, position: Vec3, color: Vec3):
        self.position = position
        self.color = color


class Scene:
    def __init__(self):
        self.lights = []
        self.meshes = []

    def add_light(self, light: Light):
        self.lights.append(light)

    def add_mesh(self, mesh: Mesh):
        # change the group of each mesh so that includes the light
        self.meshes.append(mesh)