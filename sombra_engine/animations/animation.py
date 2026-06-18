from dataclasses import dataclass
import numpy as np
from pyglet.enums import AnimationChannelTargetPath, AnimationInterpolation
from pyglet.model.codecs.gltf import (
    Animation as PygletAnimation,
    AnimationSampler
)
from pyglet.math import Mat4, Quaternion, Vec3


@dataclass
class AnimationChannel:
    timestamps: np.ndarray
    values: np.ndarray
    interpolation: AnimationInterpolation


class Animation:
    translation_channels: dict[int, AnimationChannel]
    rotation_channels: dict[int, AnimationChannel]
    scale_channels: dict[int, AnimationChannel]
    length: float

    def __init__(self, animation_data: PygletAnimation):
        for channel in animation_data.channels:
            sampler: AnimationSampler = channel.sampler
            timestamps_bytes = sampler.input.read()
            timestamps = np.frombuffer(timestamps_bytes, dtype='<f4')
            values_bytes = sampler.output.read()
            values = np.frombuffer(values_bytes, dtype='<f4')
            match channel.target.path:
                case AnimationChannelTargetPath.TRANSLATION:
                    values.reshape(-1, 3)
                    channels_dict = self.translation_channels
                case AnimationChannelTargetPath.ROTATION:
                    values.reshape(-1, 4)
                    channels_dict = self.rotation_channels
                case AnimationChannelTargetPath.SCALE:
                    values.reshape(-1, 3)
                    channels_dict = self.scale_channels
                case _:
                    raise Exception(
                        f"Animation channel target path invalid "
                        f"{channel.target.path}"
                    )
            new_channel = AnimationChannel(
                timestamps=timestamps,
                values=values,
                interpolation=channel.sampler.interpolation
            )
            bone_idx = channel.target.node.index
            channels_dict[bone_idx] = new_channel

    def interpolate_vec3(
        self,
        a: np.ndarray,
        b: np.ndarray,
        t: float,
        interpolation: AnimationInterpolation
    ):
        match interpolation:
            case AnimationInterpolation.LINEAR:
                value = (1 - t) * a + t * b
            case _:
                value = a
        return Vec3(value[0], value[1], value[2])

    def get_local_transform(self, bone_idx: int, time: float) -> Mat4:
        # Translation
        channel = self.translation_channels[bone_idx]
        timestamps = channel.timestamps
        n = len(timestamps)
        i = 0
        while i < n - 1:
            if timestamps[i] <= time < timestamps[i + 1]:
                break
            i += 1
        t = time - timestamps[i] / (timestamps[i + 1] - timestamps[i])
        a = channel.values[i]
        b = channel.values[i + 1]
        translation_vec = self.interpolate_vec3(a, b, t, channel.interpolation)
        translation = Mat4.from_translation(translation_vec)

        # Rotation
        # TODO

        # Scale

        return translation

