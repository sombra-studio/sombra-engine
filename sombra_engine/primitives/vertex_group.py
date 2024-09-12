from sombra_engine.primitives import Material, Triangle


class VertexGroup:
    def __init__(
        self,
        name: str,
        triangles: list[Triangle],
        material: Material
    ):
        self.name = name
        self.triangles = triangles
        self.material = material
