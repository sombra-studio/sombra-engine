from math import cos, sin, radians
import pyglet
from pyglet.math import Mat4, Vec3, clamp
from pyglet.window import key
import weakref


SENSITIVITY = 0.3


class FPSCamera:
    def __init__(
        self, window,
        position=Vec3(0.0, 2.0, -2.0),
        target=Vec3(0.0, 0.0, 0.0),
        up=Vec3(0.0, 1.0, 0.0),
        pitch=90.0,
        yaw=90.0
    ):
        self.position = position
        self.target = target
        self.up = up

        self.speed = 10.0

        self.pitch = pitch
        self.yaw = yaw

        self.input_map = {
            key.W: "forward",
            key.S: "backward",
            key.A: "left",
            key.D: "right",
        }

        self.forward = False
        self.backward = False
        self.left = False
        self.right = False

        self._window = weakref.proxy(window)
        self._window.view = Mat4.look_at(position, target, up)
        self._window.push_handlers(self)

    def on_resize(self, width, height):
        self._window.viewport = (0, 0, *self._window.get_framebuffer_size())
        self._window.projection = Mat4.perspective_projection(
            self._window.aspect_ratio, z_near=0.1, z_far=1000, fov=45
        )
        return pyglet.event.EVENT_HANDLED

    def on_refresh(self, dt):
        # Movement
        speed = self.speed * dt
        if self.forward:
            self.position += (self.target * speed)
        if self.backward:
            self.position -= (self.target * speed)
        if self.left:
            self.position -= (self.target.cross(self.up).normalize() * speed)
        if self.right:
            self.position += (self.target.cross(self.up).normalize() * speed)

        # Look

        phi = radians(self.yaw)
        theta = radians(self.pitch)
        self.target = Vec3(
            sin(theta) * cos(phi),
            cos(theta),
            sin(theta) * sin(phi)
        )

        eye = Vec3(*self.position)
        center = Vec3(*(self.position + self.target))
        up = Vec3(*self.up)

        self._window.view = Mat4.look_at(eye, center, up)

    # Mouse input

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, mod):
        self.yaw += dx * SENSITIVITY
        self.pitch = clamp(self.pitch - dy * SENSITIVITY, 0, 189.0)

    # Keyboard input

    def on_key_press(self, symbol, mod):
        if symbol in self.input_map:
            setattr(self, self.input_map[symbol], True)
        elif symbol == key.P:
            print(f"position: {self.position}")
            print(f"pitch: {self.pitch}, yaw: {self.yaw}")

    def on_key_release(self, symbol, mod):
        if symbol in self.input_map:
            setattr(self, self.input_map[symbol], False)
