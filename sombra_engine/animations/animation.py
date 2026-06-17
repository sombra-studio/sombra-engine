from dataclasses import dataclass
import numpy as np
from pyglet.math import Mat4


@dataclass
class AnimationChannel:
    timestamps: np.ndarray
    values: np.ndarray

@dataclass
class Animation:
    translation_channels: list[AnimationChannel]
    rotation_channels: list[AnimationChannel]
    scale_channels: list[AnimationChannel]
    length: float

    def get_local_transform(self, bone_idx: int, time: float) -> Mat4:
        # TODO
        pass
