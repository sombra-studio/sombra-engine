from sombra_engine.primitives import Material


class VertexGroup:
    def __init__(self, name: str, indices: list[int], material: Material):
        self.name = name
        self.indices = indices
        self.material = material
