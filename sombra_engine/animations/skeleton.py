from dataclasses import dataclass
from pyglet.math import Mat4


@dataclass
class Bone:
    idx: int
    name: str
    local_bind_transform: Mat4
    inverse_bind_transform: Mat4
    children: list[Bone] | None = None


@dataclass
class Skeleton:
    bones: list[Bone]
    root_idx: int
