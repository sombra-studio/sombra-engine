import os
import psutil
from pudu_ui import Label, LabelParams, Widget
from pudu_ui.styles.fonts import FontStyle
import pudu_ui
from pyglet.graphics import Batch, Group
from pyglet.window import FPSDisplay, Window



DEBUG_FONT_SIZE = 14
TIME_TO_UPDATE_DEBUG = 0.5


class Stats(Widget):
    def __init__(self, window: Window, batch: Batch, group: Group):
        super().__init__()
        self.fps_display = FPSDisplay(window, color=(0, 127, 0, 127))
        self.fps_display.label.font_size = DEBUG_FONT_SIZE
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
            batch=batch,
            group=group
        )
        self.batch = batch
        self.time_to_update_debug = TIME_TO_UPDATE_DEBUG
        self.process = psutil.Process(os.getpid())

    def draw(self):
        self.fps_display.draw()
        self.batch.draw()

    def update(self, dt: float):
        self.time_to_update_debug -= dt
        if self.time_to_update_debug <= 0:
            self.time_to_update_debug = TIME_TO_UPDATE_DEBUG
            ram_used = self.process.memory_info().rss / (1024 * 1024)  # in MB
            self.memory_label.text = f"{round(ram_used, 2)} MB"
            self.memory_label.invalidate()

        self.memory_label.update(dt)
