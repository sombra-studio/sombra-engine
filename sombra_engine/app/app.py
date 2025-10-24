import os
import psutil
from pudu_ui.styles.fonts import FontStyle
from pudu_ui import Label, LabelParams
import pudu_ui
from pyglet.event import EVENT_HANDLED
from pyglet.gl import (
    GL_CULL_FACE, GL_DEPTH_TEST, GL_LESS, glClearColor, glDepthFunc,
    glDisable, glEnable
)
from pyglet.graphics import Batch, Group
from pyglet.math import Mat4, Vec3
from pyglet.window import FPSDisplay, key, Window
import pyglet


from sombra_engine.camera import FPSCamera
from sombra_engine.debug import Gizmo


DEBUG_FONT_SIZE = 14
TIME_TO_UPDATE_DEBUG = 0.5


class App(Window):
    def __init__(
        self,
        caption: str = "Sombra Engine",
        is_debug: bool = False
    ):
        super().__init__(caption=caption, vsync=False)
        self.is_debug = is_debug
        self.fps_display = FPSDisplay(self, color=(0, 127, 0, 127))
        self.fps_display.label.font_size = DEBUG_FONT_SIZE
        self.camera = FPSCamera(
            self, position=Vec3(0.0, 0.0, 15.0), pitch=90, yaw=-90
        )
        self.batch = Batch()
        self.debug_group = Group()
        self.debug_group.visible = is_debug

        self.gizmo = Gizmo(size=10.0, batch=self.batch, group=self.debug_group)
        self.debug_ui_batch = Batch()
        self.ui_projection = Mat4.orthogonal_projection(
            0.0, self.width, 0.0, self.height,
            0.0, 1000.0
        )
        debug_label_style = FontStyle(
            font_size=DEBUG_FONT_SIZE,
            weight=pudu_ui.styles.fonts.Weight.BOLD,
            color=pudu_ui.colors.Color(0, 127, 0),
            opacity=127
        )
        y = 30
        memory_label_params = LabelParams(
            x=self.fps_display.label.x,
            y=y,
            style=debug_label_style
        )
        self.memory_label = Label(
            params=memory_label_params,
            batch=self.debug_ui_batch,
            group=self.debug_group
        )
        self.time_to_update_debug = TIME_TO_UPDATE_DEBUG
        self.process = psutil.Process(os.getpid())

    def draw_2d_debug_ui(self):
        temp_proj = self.projection
        temp_view = self.view
        self.projection = self.ui_projection
        self.view = Mat4()

        # Needs to disable DEPTH TEST for 2D UI
        glDisable(GL_DEPTH_TEST)
        self.fps_display.draw()
        self.debug_ui_batch.draw()

        self.projection = temp_proj
        self.view = temp_view

    def on_draw(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clear()
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
        self.time_to_update_debug -= dt
        if self.time_to_update_debug <= 0:
            self.time_to_update_debug = TIME_TO_UPDATE_DEBUG
            ram_used = self.process.memory_info().rss / (1024 * 1024)  # in MB
            self.memory_label.text = f"{round(ram_used, 2)} MB"
            self.memory_label.invalidate()

        self.memory_label.update(dt)

    def run(self, interval: float = 1.0 / 60.0):
        if not interval:
            pyglet.clock.schedule(self.update)
        else:
            pyglet.clock.schedule_interval(self.update, interval)
        pyglet.app.run(interval)
