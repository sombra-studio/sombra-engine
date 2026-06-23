from dataclasses import dataclass
from pyglet.math import Mat4


@dataclass
class Bone:
    idx: int = 0
    name: str = 'undefined'
    local_bind_transform: Mat4 = Mat4()
    inverse_bind_transform: Mat4 = Mat4()
    children: list[Bone] | None = None


@dataclass
class Skeleton:
    bones: list[Bone]
    root_idx: int
