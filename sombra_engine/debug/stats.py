import os
import psutil
from pudu_ui import Label, LabelParams, Params, Widget
from pudu_ui.layouts import ListDirection, ListLayout, ListLayoutParams
from pudu_ui.styles.fonts import FontStyle
import pudu_ui
from pyglet.graphics import Batch, Group
from pyglet.window import FPSDisplay, Window


DEBUG_FONT_SIZE = 14
TIME_TO_UPDATE_DEBUG = 0.5
LABEL_Y_MARGIN = 22
INTER_ITEM_SPACING = 1


class Stats(Widget):
    def __init__(
        self, window: Window, params: Params, batch: Batch, group: Group
    ):
        super().__init__(params=params, batch=batch, group=group)
        self.window = window
        self.fps_display = FPSDisplay(
            window=window, color=(0, 127, 0, 127), batch=batch
        )
        self.fps_label = self.fps_display.label
        self.fps_label.position = (self.x, self.y, 0.0)
        self.fps_label.font_size = DEBUG_FONT_SIZE
        debug_label_style = FontStyle(
            font_size=DEBUG_FONT_SIZE,
            weight="bold",
            color=pudu_ui.colors.Color(0, 127, 0),
            opacity=127
        )

        label_params = LabelParams(
            text="hola",
            style=debug_label_style
        )
        self.memory_label = Label(
            params=label_params,
            batch=batch,
            group=group,
            parent=self
        )
        self.resolution_label = Label(
            params=label_params,
            batch=batch,
            group=group,
            parent=self
        )
        self.tri_count_label = Label(
            params=label_params,
            batch=batch,
            group=group,
            parent=self
        )

        list_layout_params = ListLayoutParams(
            y=LABEL_Y_MARGIN,
            width=params.width,
            height=params.height - LABEL_Y_MARGIN,
            inter_item_spacing=INTER_ITEM_SPACING,
            resizes_item_height=False,
            direction=ListDirection.VERTICAL
        )
        self.list_layout = ListLayout(
            params=list_layout_params,
            batch=batch,
            group=group,
            parent=self
        )

        # Add children widgets
        self.children.append(self.list_layout)
        self.children.append(self.memory_label)
        self.children.append(self.resolution_label)
        self.children.append(self.tri_count_label)

        # Add to list layout
        self.list_layout.add(self.memory_label)
        self.list_layout.add(self.resolution_label)
        self.list_layout.add(self.tri_count_label)

        n = len(self.list_layout.children)
        self.list_layout.height = (
            n *
            self.tri_count_label.impl.content_height +
            (n - 1) * INTER_ITEM_SPACING
        )
        self.list_layout.invalidate()

        self.batch = batch
        self.time_to_update_debug = TIME_TO_UPDATE_DEBUG
        self.process = psutil.Process(os.getpid())

    def draw(self):
        self.fps_display.draw()
        if isinstance(self.batch, Batch):
            self.batch.draw()

    def update(self, dt: float):
        self.time_to_update_debug -= dt
        if self.time_to_update_debug <= 0:
            self.time_to_update_debug = TIME_TO_UPDATE_DEBUG
            ram_used = self.process.memory_info().rss / (1024 * 1024)  # in MB
            self.memory_label.text = f"{round(ram_used, 2)} MB"
            self.memory_label.invalidate()
            self.invalidate()

        self.set_resolution()
        super().update(dt)

    def set_tri_counts(self, tri_count: int):
        self.tri_count_label.text = f"{tri_count:,} triangles"
        self.tri_count_label.invalidate()

    def set_resolution(self):
        self.resolution_label.text = (
            f"{self.window.width}x"
            f"{self.window.height} "
            f"pxs"
        )
        self.resolution_label.invalidate()
