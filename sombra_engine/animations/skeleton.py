from dataclasses import dataclass, field
from pyglet.math import Mat4




@dataclass
class Bone:
    idx: int = 0        # the index of its nodes in the nodes array
    bone_idx: int = 0   # the index in the skeleton.bones array
    name: str = 'undefined'
    local_bind_transform: Mat4 = Mat4()
    inverse_bind_transform: Mat4 = Mat4()
    children: list[Bone] = field(default_factory=list)


@dataclass
class Skeleton:
    bones: list[Bone]
    root: Bone
