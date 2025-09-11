from dataclasses import dataclass


from sombra_engine.primitives import Transform


@dataclass
class Pose:
    bones_transforms: list[Transform]


@dataclass
class Keyframe:
    pose: Pose
    time: float


@dataclass
class Animation:
    keyframes: list[Keyframe]
    length: float
