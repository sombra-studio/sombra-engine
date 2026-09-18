from importlib.resources import files

from pyglet.enums import ComponentFormat, FramebufferAttachment, TextureFilter, AddressMode
from pyglet.graphics.framebuffer import Framebuffer
from pyglet.graphics import Batch, Texture, Shader, ShaderProgram
from pyglet.sprite import Sprite
import pyglet


from sombra_engine.models.gltf import GLTFLoader
from sombra_engine.models.obj import OBJLoader


SHADOW_MAP_WIDTH = 1024
SHADOW_MAP_HEIGHT = 1024


if __name__ == '__main__':
    pyglet.resource.path.append("./tests/data/")
    pyglet.resource.reindex()

    window = pyglet.window.Window()
    box_scenes, _, __ = GLTFLoader.load('box.glb')
    plane_scene = OBJLoader.load('plane.obj')

    # Draw into a quad
    shadows_batch: Batch = Batch()
    shadows_framebuffer: Framebuffer = Framebuffer()
    shadow_map = Texture.create(
        width=SHADOW_MAP_WIDTH,
        height=SHADOW_MAP_HEIGHT,
        internal_format=ComponentFormat.D,
        internal_format_size=16,
        filters=TextureFilter.NEAREST,
        address_mode=AddressMode.CLAMP_TO_BORDER
    )

    shadows_framebuffer.attach_texture(
        shadow_map,
        attachment=FramebufferAttachment.DEPTH
    )
    quad = Sprite(shadow_map)

    # Shadow Map Program
    # Create program
    shadow_map_vs_str = files('sombra_engine.shaders').joinpath(
        'depth.vert'
    ).read_text()
    shadow_map_vs = Shader(shadow_map_vs_str, shader_type='vertex')
    shadow_map_fs_str = files('sombra_engine.shaders').joinpath(
        'empty.frag'
    ).read_text()
    shadow_map_fs = Shader(shadow_map_fs_str, shader_type='fragment')
    shadow_map_program: ShaderProgram = ShaderProgram(
        shadow_map_vs, shadow_map_fs
    )

    @window.event
    def on_draw():
        window.clear()
        # Shadow pass
        shadows_framebuffer.clear()
        with shadows_batch.draw_with_options() as options:
            options.framebuffer = shadows_framebuffer
            options.viewport = (0, 0, SHADOW_MAP_WIDTH, SHADOW_MAP_HEIGHT)

        # Normal pass
        quad.draw()

    pyglet.app.run()



