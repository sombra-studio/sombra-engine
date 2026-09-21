from pudu_ui import Params
from pudu_ui.colors import Color, BLACK
import pudu_ui
from pyglet.enums import ComponentFormat, FramebufferAttachment, TextureFilter, AddressMode
from pyglet.event import EVENT_HANDLED
from pyglet.graphics.api.gl.gl import (
    GL_DEPTH_BUFFER_BIT, GL_CULL_FACE, GL_DEPTH_TEST, GL_LESS, GL_NONE,
    glClear, glClearColor, glDepthFunc, glDisable, glDrawBuffer, glEnable,
    glViewport
)
from pyglet.graphics import Batch, Group, Framebuffer, Texture
from pyglet.math import Mat4, Vec3
from pyglet.window import key
from pyglet.window.camera import FPSCamera
import pyglet


from sombra_engine import Scene
# from sombra_engine.camera import FPSCamera
from sombra_engine.debug import Gizmo, Stats
from sombra_engine.models import SkeletalMesh
from sombra_engine.fpscamera import FPSCameraControls


DEPTH_MAP_WIDTH = 1024
DEPTH_MAP_HEIGHT = 1024


class App(pudu_ui.App):
    def __init__(
        self,
        width: int = 1280,
        height: int = 720,
        caption: str = "Sombra Engine",
        update_rate: float = 1.0 / 60.0,
        background_color: Color = BLACK,
        vsync: bool = True,
        is_debug: bool = False
    ):
        super().__init__(
            width=width,
            height=height,
            caption=caption,
            update_rate=update_rate,
            background_color=background_color,
            vsync=vsync,
            is_debug=is_debug
        )
        self.fps_camera = FPSCamera(
            self,
            position=Vec3(0.0, 1.0, 6.0),
            target=Vec3(0.0, 1.0, 0.0),
        )
        self.controls = FPSCameraControls(self, self.fps_camera)
        if controllers := pyglet.input.get_controllers():
            controller = controllers[0]
            controller.open()
            controller.push_handlers(self.controls)
        self.batch = Batch()
        self.shadows_batch: Batch = Batch()
        self.shadows_framebuffer = Framebuffer()
        self.depth_map = Texture.create(
            width=DEPTH_MAP_WIDTH,
            height=DEPTH_MAP_HEIGHT,
            internal_format=ComponentFormat.D,
            internal_format_size=32,
            internal_format_type='f',
            filters=TextureFilter.NEAREST,
            address_mode=AddressMode.CLAMP_TO_BORDER
        )
        self.shadows_framebuffer.attach_texture(
            self.depth_map,
            attachment=FramebufferAttachment.DEPTH
        )
        self.shadows_framebuffer.bind()
        glDrawBuffer(GL_NONE)
        self.shadows_framebuffer.unbind()

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

        self.scenes: list[Scene] = []
        self.current_scene: Scene | None = None
        self.light_projection: Mat4 = Mat4()
        self.light_view: Mat4 = Mat4()
        self.tri_count = 0

    def set_scene(self, scene: Scene):
        self.current_scene = scene
        self.tri_count = 0
        for mesh in scene.meshes:
            self.tri_count += mesh.tri_count
        self.stats.set_tri_counts(self.tri_count)

    def draw_2d_debug_ui(self):
        temp_proj = self.projection
        temp_view = self.view
        self.projection = self.ui_projection
        self.view = Mat4()

        # Needs to disable DEPTH TEST for 2D UI
        glDisable(GL_DEPTH_TEST)
        self.debug_ui_batch.draw()

        self.projection = temp_proj
        self.view = temp_view

    def on_draw(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clear()

        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        # Shadow Pass
        glViewport(0, 0, DEPTH_MAP_WIDTH, DEPTH_MAP_HEIGHT)
        self.shadows_framebuffer.bind()
        glClear(GL_DEPTH_BUFFER_BIT)
        self.shadows_batch.draw()
        self.shadows_framebuffer.unbind()
        # with self.shadows_batch.draw_with_options() as options:
        #     options.framebuffer = self.shadows_framebuffer
        #     options.viewport = (0, 0, SHADOWS_MAP_WIDTH, SHADOWS_MAP_HEIGHT)

        # Normal Pass
        if self.is_debug:
            with self.gizmo.batch.draw_with_options() as options:
                options.camera = self.fps_camera

        with self.batch.draw_with_options() as options:
            options.camera = self.fps_camera

        if self.is_debug:
            # Use 2D UI here
            self.draw_2d_debug_ui()
        return EVENT_HANDLED

    def on_key_press(self, symbol, mod):
        handled = super().on_key_press(symbol, mod)
        if not handled:
            if mod & key.MOD_SHIFT and symbol == key.P:
                pyglet.graphics.framebuffer.get_screenshot().save(
                    'docs/screenshot.png'
                )
                handled = EVENT_HANDLED
            if symbol == key.SPACE:
                self.is_paused = not self.is_paused

        return handled

    def update(self, dt: float):
        super().update(dt)
        if self.is_paused:
            return
        self.stats.update(dt)

        # Update models
        if self.current_scene and self.current_scene.meshes:
            for mesh in self.current_scene.meshes:
                if isinstance(mesh, SkeletalMesh):
                    # Update skeletal meshes
                    mesh.update(dt)

                # Update eye uniform from camera
                if 'eye' in mesh.program.uniforms:
                    mesh.program['eye'] = self.fps_camera.position
