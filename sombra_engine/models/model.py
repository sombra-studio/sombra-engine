from sombra_engine.primitives import *
from .mesh import Mesh


class Model:
    def __init__(
        self, name: str, meshes: list[Mesh], transform: Transform = Transform(),
        parent: SceneObject = None
    ):
        self.name = name
        self.meshes = meshes
        self.transform = transform
        self.parent = parent
        self.tri_count: int = 0
        self.calculate_tri_count()

    def calculate_tri_count(self):
        self.tri_count = 0
        for mesh in self.meshes:
            self.tri_count += mesh.tri_count

    def draw(self):
        for mesh in self.meshes:
            mesh.draw()

    def update(self, dt: float):
        for mesh in self.meshes:
            mesh.update(dt)
