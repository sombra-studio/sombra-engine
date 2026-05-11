from dataclasses import dataclass
import numpy as np


@dataclass
class Pose:
    translations: np.ndarray
    scales: np.ndarray
    rotations: np.ndarray


@dataclass
class Keyframe:
    pose: Pose
    time: float


@dataclass
class Animation:
    keyframes: list[Keyframe]
    length: float
