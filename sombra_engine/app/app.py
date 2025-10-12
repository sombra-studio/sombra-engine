from pyglet.event import EVENT_HANDLE_STATE, EVENT_HANDLED
from pyglet.gl import (
    GL_CULL_FACE, GL_DEPTH_TEST, GL_LESS, glDepthFunc,
    glEnable
)
from pyglet.graphics import Batch, Group
from pyglet.math import Vec3
from pyglet.window import FPSDisplay, Window


from sombra_engine.camera import FPSCamera
from sombra_engine.debug import Gizmo


class App(Window):
    def __init__(self, is_debug: bool = False):
        super().__init__(caption="Sombra Engine")
        self.is_debug = is_debug
        self.fps_display = FPSDisplay(self, color=(0, 127, 0, 127))
        self.camera = FPSCamera(
            self, position=Vec3(0.0, 0.0, -15.0), pitch=90, yaw=90
        )
        self.batch = Batch()
        self.debug_group = Group()
        self.gizmo = Gizmo(size=10.0, batch=self.batch, group=self.debug_group)
        self.debug_group.visible = is_debug

    def on_draw(self) -> EVENT_HANDLE_STATE:
        self.clear()
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        self.batch.draw()
        if self.is_debug:
            # TODO: Need to use ortho projection here
            self.fps_display.draw()
        return EVENT_HANDLED
