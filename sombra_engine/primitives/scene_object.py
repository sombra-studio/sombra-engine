from pyglet.math import Mat4


from sombra_engine.primitives import Transform


class SceneObject:
    def __init__(self, transform: Transform = Transform()):
        self.transform = transform

    def get_matrix(self) -> Mat4:
        return self.transform.get_matrix()
