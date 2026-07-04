from dataclasses import dataclass
from pyglet.enums import AnimationChannelTargetPath, AnimationInterpolation
from pyglet.model.codecs.gltf import (
    Animation as PygletAnimation,
    AnimationSampler
)
from pyglet.math import Mat4, Quaternion, Vec3


from sombra_engine import utils


@dataclass
class AnimationChannel:
    timestamps: list[float]
    max_time: float
    values: list[Vec3] | list[Quaternion]
    interpolation: AnimationInterpolation
    path: AnimationChannelTargetPath


def interpolate_vec3(
    a: Vec3,
    b: Vec3,
    t: float,
    interpolation: AnimationInterpolation
):
    match interpolation:
        case AnimationInterpolation.LINEAR:
            value = (1 - t) * a + t * b
        case _:
            value = a
    return value


def interpolate_quat(
    a: Quaternion,
    b: Quaternion,
    t: float,
    interpolation: AnimationInterpolation
):
    match interpolation:
        case AnimationInterpolation.LINEAR:
            value = utils.slerp(a, b, t)
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
            quat = interpolate_quat(a, b, t, channel.interpolation)
            return quat.to_mat4()
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
            timestamps = sampler.input.as_array().tolist()
            values_arr = sampler.output.as_array()

            match channel.target.path:
                case AnimationChannelTargetPath.TRANSLATION:
                    channels_dict = self.translation_channels
                    values = []
                    for i in range(0, len(values_arr), 3):
                        vec = Vec3(
                            values_arr[i],
                            values_arr[i + 1],
                            values_arr[i + 2]
                        )
                        values.append(vec)
                case AnimationChannelTargetPath.ROTATION:
                    channels_dict = self.rotation_channels
                    values = []
                    for i in range(0, len(values_arr), 4):
                        quat = Quaternion(
                            values_arr[i + 3],
                            values_arr[i],
                            values_arr[i + 1],
                            values_arr[i + 2],
                        )
                        values.append(quat)
                case AnimationChannelTargetPath.SCALE:
                    channels_dict = self.scale_channels
                    values = []
                    for i in range(0, len(values_arr), 3):
                        vec = Vec3(
                            values_arr[i],
                            values_arr[i + 1],
                            values_arr[i + 2]
                        )
                        values.append(vec)
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
            node_idx = channel.target.node.index
            channels_dict[node_idx] = new_channel

    def get_local_transform(self, node_idx: int, time: float) -> Mat4:
        # Translation
        channel = self.translation_channels[node_idx]
        translation = get_transform(channel, time)

        # Rotation
        channel = self.rotation_channels[node_idx]
        rotation = get_transform(channel, time)

        # Scale
        channel = self.scale_channels[node_idx]
        scale = get_transform(channel, time)

        local_transform = translation @ rotation @ scale
        return local_transform

