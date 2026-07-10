import math
from pyglet.math import Quaternion
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



def slerp(a: Quaternion , b: Quaternion , t: float) -> Quaternion:
    dot = a.dot(b)

    if dot < 0.0:
        b = b * -1
        dot = -dot

    if dot > 0.9995:
        out = a * (1 - t) + b * t
        out = out.normalize()
        return out

    theta_0 = math.acos(dot)
    sin_theta_0 = math.sin(theta_0)
    theta = theta_0 * t
    sin_theta = math.sin(theta)

    s0 = math.cos(theta) - dot * sin_theta / sin_theta_0
    s1 = sin_theta / sin_theta_0

    out = a * s0 + b * s1

    return out
