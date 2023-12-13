from pyglet.math import Vec3
from math import acos, asin, cos, radians, sin, sqrt
import math


SPEED: float = 30.0
SENSITIVITY: float = 0.3


class Camera:
    def __init__(
        self,
        position: Vec3 = Vec3(0.0, 0.0, -1.0),
        up: Vec3 = Vec3(0.0, 1.0, 0.0),
        target: Vec3 = Vec3(),
        speed: float = SPEED,
        sensitivity: float = SENSITIVITY
    ):
        self.position = position
        self.up = up
        self.target = target
        self.speed = speed
        self.sensitivity = sensitivity
        self.forward: bool = False
        self.backward: bool = False
        self.left: bool = False
        self.right: bool = False

        # Calculate direction from target and position
        self.direction: Vec3 = (target - position).normalize()

        # Calculate theta angle from direction
        dir_projection_xz = sqrt(self.direction.x ** 2 + self.direction.z ** 2)
        self.theta: float = 0.0
        if dir_projection_xz:
            self.theta = acos(self.direction.x / dir_projection_xz)
        if self.direction.z < 0.0:
            # If the direction of the camera is in negative z, theta can only
            # be in between the PI and 2 x PI range
            self.theta += math.pi

        # Calculate phi angle from direction
        self.phi: float = 0.0
        dir_projection_yz = sqrt(self.direction.y ** 2 + self.direction.z ** 2)
        if dir_projection_yz:
            self.phi = asin(self.direction.y / dir_projection_yz)

    def update(self, dt):
        pass
