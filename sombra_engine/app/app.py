from pyglet.event import EVENT_HANDLED
from pyglet.gl import (
    GL_CULL_FACE, GL_DEPTH_TEST, GL_LESS, glDepthFunc, glDisable, glEnable
)
from pyglet.graphics import Batch, Group
from pyglet.math import Mat4, Vec3
from pyglet.window import FPSDisplay, Window


from sombra_engine.camera import FPSCamera
from sombra_engine.debug import Gizmo


class App(Window):
    def __init__(self, is_debug: bool = False):
        super().__init__(caption="Sombra Engine", vsync=False)
        self.is_debug = is_debug
        self.fps_display = FPSDisplay(self, color=(0, 127, 0, 127))
        self.camera = FPSCamera(
            self, position=Vec3(0.0, 0.0, -15.0), pitch=90, yaw=90
        )
        self.batch = Batch()
        self.debug_group = Group()
        self.gizmo = Gizmo(size=10.0, batch=self.batch)
        self.debug_group.visible = is_debug
        self.ui_projection = Mat4.orthogonal_projection(
            0.0, self.width, 0.0, self.height,
            0.0, 1000.0
        )

    def draw_2d_debug_ui(self):
        temp_proj = self.projection
        temp_view = self.view
        self.projection = self.ui_projection
        self.view = Mat4()

        # Needs to disable DEPTH TEST for 2D UI
        glDisable(GL_DEPTH_TEST)
        self.fps_display.draw()

        self.projection = temp_proj
        self.view = temp_view

    def on_draw(self):
        self.clear()
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        self.batch.draw()
        if self.is_debug:
            # Use 2D UI here
            self.draw_2d_debug_ui()
        return EVENT_HANDLED
