from pudu_ui import Params
from pyglet.event import EVENT_HANDLED
from pyglet.gl import (
    GL_CULL_FACE, GL_DEPTH_TEST, GL_LESS, glClearColor, glDepthFunc,
    glDisable, glEnable
)
from pyglet.graphics import Batch, Group
from pyglet.math import Mat4, Vec3
from pyglet.window import key, Window
import pyglet


from sombra_engine.camera import FPSCamera
from sombra_engine.debug import Gizmo, Stats
from sombra_engine.models import Model


class App(Window):
    def __init__(
        self,
        caption: str = "Sombra Engine",
        is_debug: bool = False
    ):
        super().__init__(caption=caption, vsync=False)
        self.is_debug = is_debug
        self.camera = FPSCamera(
            self, position=Vec3(0.0, 0.0, 15.0), pitch=90, yaw=-90
        )
        self.batch = Batch()
        self.debug_group = Group()
        self.debug_group.visible = is_debug

        self.gizmo = Gizmo(size=10.0)
        self.debug_ui_batch = Batch()
        self.ui_projection = Mat4.orthogonal_projection(
            0.0, self.width, 0.0, self.height,
            0.0, 1000.0
        )
        stats_params = Params(x=10.0, y=10.0)
        self.stats = Stats(
            self, stats_params, self.debug_ui_batch, self.debug_group
        )

        self.models: list[Model] = []
        self.tri_count = 0

    def add_model(self, model: Model):
        self.models.append(model)
        self.tri_count += model.tri_count
        self.stats.set_tri_counts(self.tri_count)

    def draw_2d_debug_ui(self):
        temp_proj = self.projection
        temp_view = self.view
        self.projection = self.ui_projection
        self.view = Mat4()

        # Needs to disable DEPTH TEST for 2D UI
        glDisable(GL_DEPTH_TEST)
        self.stats.draw()

        self.projection = temp_proj
        self.view = temp_view

    def on_draw(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clear()

        # Draw gizmo first
        glDisable(GL_DEPTH_TEST)
        self.gizmo.draw()

        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        self.batch.draw()
        if self.is_debug:
            # Use 2D UI here
            self.draw_2d_debug_ui()
        return EVENT_HANDLED

    def on_key_press(self, symbol, mod):
        handled = super().on_key_press(symbol, mod)
        if not handled:
            if mod & key.MOD_SHIFT and symbol == key.P:
                pyglet.image.get_buffer_manager().get_color_buffer().save(
                    'docs/screenshot.png'
                )
                handled = EVENT_HANDLED
        return handled

    def update(self, dt: float):
        self.stats.update(dt)

        # Update models
        for model in self.models:
            model.update(dt)

    def run(self, interval: float = 1.0 / 60.0):
        if not interval:
            pyglet.clock.schedule(self.update)
        else:
            pyglet.clock.schedule_interval(self.update, interval)
        pyglet.app.run(interval)
