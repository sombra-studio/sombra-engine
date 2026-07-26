from pyglet.math import Mat4
from typing import Self

from sombra_engine.primitives import Transform


class SceneObject:
    def __init__(
        self,
        name: str = "undefined",
        transform: Transform = Transform(),
        matrix: Mat4 = Mat4(),
        parent: Self | None = None
    ):
        """
        SceneObject could be any object that is in a Scene and has a
        Transform that stores scale, rotation and translation or / and a matrix.
        You should use only one of those.

        Parenting is available, to define relative coordinates.

        The idea of this class is that other can inherit from it like Light,
        Camera, Mesh, etc.

        Args:
            transform: A Transform instance that defines the scale, rotation
                and translation.
            matrix: A Mat4 instance that can be used instead of transform to
                define the transformation matrix of this object
            parent: A reference to the parent object, it could be null
        """
        self.name = name
        self.transform = transform
        self.matrix = matrix
        self.parent = parent
        self.children: list[SceneObject] = []

    def get_matrix(self) -> Mat4:
        if self.parent:
            answer = (
                self.parent.get_matrix() @
                self.matrix @
                self.transform.get_matrix()
            )
            return answer
        return self.matrix @ self.transform.get_matrix()
