import math
import numpy as np
import pyglet


def create_color_tex(color: tuple[int, int, int, int]) -> pyglet.graphics.Texture:
    color_pattern = pyglet.image.SolidColorImagePattern(color)
    img = color_pattern.create_image(16, 16)
    return img.get_texture()

def create_black_tex() -> pyglet.graphics.Texture:
    return create_color_tex((0, 0, 0, 255))

def create_blue_tex() -> pyglet.graphics.Texture:
    return create_color_tex((0, 0, 255, 255))

def create_white_tex() -> pyglet.graphics.Texture:
    return create_color_tex((255, 255, 255, 255))

def create_gray_tex() -> pyglet.graphics.Texture:
    return create_color_tex((123, 123, 123, 255))


def slerp(a: np.ndarray, b: np.ndarray, t: float, out: np.ndarray) -> None:
    dot = a[0] * b[0] + a[1] * b[1] + a[2] * b[2] + a[3] * b[3]

    if dot < 0.0:
        b0, b1, b2, b3 = -b[0], -b[1], -b[2], -b[3]
        dot = -dot
    else:
        b0, b1, b2, b3 = b[0], b[1], b[2], b[3]

    if dot > 0.9995:

        out[0] = a[0] + t * (b0 - a[0])
        out[1] = a[1] + t * (b1 - a[1])
        out[2] = a[2] + t * (b2 - a[2])
        out[3] = a[3] + t * (b3 - a[3])

        inv = 1.0 / math.sqrt(
            out[0] * out[0] +
            out[1] * out[1] +
            out[2] * out[2] +
            out[3] * out[3]
        )
        out[0] *= inv
        out[1] *= inv
        out[2] *= inv
        out[3] *= inv
        return

    theta_0 = math.acos(dot)
    sin_theta_0 = math.sin(theta_0)
    theta = theta_0 * t
    sin_theta = math.sin(theta)

    s0 = math.cos(theta) - dot * sin_theta / sin_theta_0
    s1 = sin_theta / sin_theta_0

    out[0] = s0 * a[0] + s1 * b0
    out[1] = s0 * a[1] + s1 * b1
    out[2] = s0 * a[2] + s1 * b2
    out[3] = s0 * a[3] + s1 * b3
