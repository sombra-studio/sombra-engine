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


def quaternion_slerp(q1: Quaternion, q2: Quaternion, t: float) -> Quaternion:
    """
    Performs Spherical Linear Interpolation between two quaternions.

    Args:
        q1: The starting Pyglet Quaternion.
        q2: The target Pyglet Quaternion.
        t: The interpolation parameter between 0.0 and 1.0.

    Returns:
        A new interpolated pyglet.math.Quaternion.
    """
    # 1. Compute the cosine of the angle between the two vectors (dot product)
    dot = q1.w * q2.w + q1.x * q2.x + q1.y * q2.y + q1.z * q2.z

    # 2. Shortest path check
    # If the dot product is negative, the quaternions have opposite handedness.
    # We negate one quaternion to take the shortest path across the sphere.
    if dot < 0.0:
        q2_w, q2_x, q2_y, q2_z = -q2.w, -q2.x, -q2.y, -q2.z
        dot = -dot
    else:
        q2_w, q2_x, q2_y, q2_z = q2.w, q2.x, q2.y, q2.z

    # 3. Lerp fallback for close quaternions
    # If the inputs are too close, linearly interpolate and normalize
    # to avoid division by zero in the slerp formula.
    if dot > 0.9995:
        w = q1.w + t * (q2_w - q1.w)
        x = q1.x + t * (q2_x - q1.x)
        y = q1.y + t * (q2_y - q1.y)
        z = q1.z + t * (q2_z - q1.z)

        # Normalize the result
        length = math.sqrt(w * w + x * x + y * y + z * z)
        return Quaternion(w / length, x / length, y / length, z / length)

    # 4. Slerp computation
    # Calculate the angle between the quaternions
    theta_0 = math.acos(dot)
    sin_theta_0 = math.sin(theta_0)

    # Calculate the scale factors for the interpolation
    s0 = math.sin((1.0 - t) * theta_0) / sin_theta_0
    s1 = math.sin(t * theta_0) / sin_theta_0

    # Compute the interpolated quaternion values
    w = s0 * q1.w + s1 * q2_w
    x = s0 * q1.x + s1 * q2_x
    y = s0 * q1.y + s1 * q2_y
    z = s0 * q1.z + s1 * q2_z

    return Quaternion(w, x, y, z)


def book_slerp(a: Quaternion , b: Quaternion , t: float) -> Quaternion:
    dot = a.dot(b)

    if dot > 0.9995:
        return a * (1 - t) + b * t

    abs_dot = abs(dot)
    x = math.acos(abs_dot)
    s = dot / abs_dot

    v = (
        a * (math.sin(x * (1 - t)) / math.sin(x)) +
        b * s * (math.sin(x * t) / math.sin(x))
    )
    return v


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
