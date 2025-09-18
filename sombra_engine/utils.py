import math as _math
from pyglet.math import Mat4
import pyglet

def create_color_tex(color: tuple[int, int, int, int]) -> pyglet.image.Texture:
    color_pattern = pyglet.image.SolidColorImagePattern(color)
    img = color_pattern.create_image(16, 16)
    return img.get_texture()

def create_black_tex() -> pyglet.image.Texture:
    return create_color_tex((0, 0, 0, 255))

def create_white_tex() -> pyglet.image.Texture:
    return create_color_tex((255, 255, 255, 255))

def create_gray_tex() -> pyglet.image.Texture:
    return create_color_tex((123, 123, 123, 255))


class Quaternion(pyglet.math.Quaternion):
    @classmethod
    def from_mat4(cls, matrix: Mat4) -> 'Quaternion':

        # 00: a, 01: b, 02: c, 03: d
        # 10: e, 11: f, 12: g, 13: h
        # 20: i, 21: j, 22: k, 23: l
        # 30: m, 31: n, 32: o, 33: p

        (a, b, c, d,
         e, f, g, h,
         i, j, k, l,
         m, n, o, p) = matrix

        (m00, m01, m02, m03,
         m10, m11, m12, m13,
         m20, m21, m22, m23,
         m30, m31, m32, m33) = matrix

        tr = m00 + m11 + m22

        if tr > 0:
            s = _math.sqrt(tr + 1.0) * 2
            w = 0.25 * s
            x = (m21 - m12) / s
            y = (m02 - m20) / s
            z = (m10 - m01) / s
        elif (m00 > m11) and (m00 > m22):
            s = _math.sqrt(1.0 + m00 - m11 - m22) * 2
            w = (m21 - m12) / s
            x = 0.25 * s
            y = (m01 + m10) / s
            z = (m02 + m20) / s
        elif m11 > m22:
            s = _math.sqrt(1.0 + m11 - m00 - m22) * 2
            w = (m02 - m20) / s
            x = (m01 + m10) / s
            y = 0.25 * s
            z = (m12 + m21) / s
        else:
            s = _math.sqrt(1.0 + m22 - m00 - m11) * 2
            w = (m10 - m01) / s
            x = (m02 + m20) / s
            y = (m12 + m21) / s
            z = 0.25 * s

        return cls(w, x, y, z)
