from dataclasses import dataclass
import numpy as np
from pyglet.enums import AnimationChannelTargetPath, AnimationInterpolation
from pyglet.model.codecs.gltf import (
    Animation as PygletAnimation,
    AnimationSampler
)
from pyglet.math import Mat4, Quaternion, Vec3

from sombra_engine import utils


@dataclass
class AnimationChannel:
    timestamps: np.ndarray
    max_time: float
    values: np.ndarray
    interpolation: AnimationInterpolation
    path: AnimationChannelTargetPath


def interpolate_vec3(
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


def interpolate_vec4(
    a: np.ndarray,
    b: np.ndarray,
    t: float,
    interpolation: AnimationInterpolation
):
    match interpolation:
        case AnimationInterpolation.LINEAR:
            value = np.array([0.0, 0.0, 0.0, 0.0], dtype='<f4')
            utils.slerp(a, b, t, value)
        case _:
            value = a
    return value


def get_transform(channel: AnimationChannel, time: float) -> Mat4:
    timestamps = channel.timestamps
    channel_time = time % channel.max_time
    i = 0
    if channel_time < timestamps[0]:
        # Clamp animation to first value until first keyframe timestamp is
        # reached
        t = 0
        a = channel.values[0]
        b = channel.values[0]
    else:
        while timestamps[i] > channel_time:
            i += 1
        match channel.interpolation:
            case AnimationInterpolation.LINEAR:
                t = (channel_time - timestamps[i]) / (
                    timestamps[i + 1] - timestamps[i]
                )
            case AnimationInterpolation.STEP:
                t = 0
            case _:
                raise ValueError(
                    f"Unknown channel interpolation {channel.interpolation}"
                )
        a = channel.values[i]
        b = channel.values[i + 1]

    match channel.path:
        case AnimationChannelTargetPath.TRANSLATION:
            vec = interpolate_vec3(a, b, t, channel.interpolation)
            return Mat4.from_translation(vec)
        case AnimationChannelTargetPath.ROTATION:
            vec = interpolate_vec4(a, b, t, channel.interpolation)
            quat = Quaternion(vec[-1], vec[0], vec[1], vec[2])
            return quat.normalize().to_mat4()
        case AnimationChannelTargetPath.SCALE:
            vec = interpolate_vec3(a, b, t, channel.interpolation)
            return Mat4.from_scale(vec)
        case _:
            raise ValueError(f"Unknown channel path {channel.path}")

class Animation:
    def __init__(self, animation_data: PygletAnimation):
        self.translation_channels: dict[int, AnimationChannel] = {}
        self.rotation_channels: dict[int, AnimationChannel] = {}
        self.scale_channels: dict[int, AnimationChannel] = {}

        for channel in animation_data.channels:
            sampler: AnimationSampler = channel.sampler
            timestamps_bytes = sampler.input.read()
            timestamps = np.frombuffer(timestamps_bytes, dtype='<f4')
            values_bytes = sampler.output.read()
            values = np.frombuffer(values_bytes, dtype='<f4')
            match channel.target.path:
                case AnimationChannelTargetPath.TRANSLATION:
                    values = values.reshape(-1, 3)
                    channels_dict = self.translation_channels
                case AnimationChannelTargetPath.ROTATION:
                    values = values.reshape(-1, 4)
                    channels_dict = self.rotation_channels
                case AnimationChannelTargetPath.SCALE:
                    values = values.reshape(-1, 3)
                    channels_dict = self.scale_channels
                case _:
                    raise Exception(
                        f"Animation channel target path invalid "
                        f"{channel.target.path}"
                    )
            new_channel = AnimationChannel(
                timestamps=timestamps,
                max_time=channel.sampler.input.max[0],
                values=values,
                interpolation=channel.sampler.interpolation,
                path=channel.target.path
            )
            bone_idx = channel.target.node.index
            channels_dict[bone_idx] = new_channel

    def get_local_transform(self, bone_idx: int, time: float) -> Mat4:
        # Translation
        channel = self.translation_channels[bone_idx]
        translation = get_transform(channel, time)

        # Rotation
        channel = self.rotation_channels[bone_idx]
        rotation = get_transform(channel, time)

        # Scale
        channel = self.scale_channels[bone_idx]
        scale = get_transform(channel, time)

        local_transform = translation @ rotation @ scale
        return local_transform

