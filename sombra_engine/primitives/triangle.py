from sombra_engine.primitives import Vertex


class Triangle:
    def __init__(self, a: Vertex, b: Vertex, c: Vertex):
        self.a = a
        self.b = b
        self.c = c
