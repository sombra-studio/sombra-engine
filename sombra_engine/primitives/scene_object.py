from sombra_engine.primitives import Transform


class SceneObject:
    def __init__(self, transform: Transform = Transform()):
        self.transform = transform
