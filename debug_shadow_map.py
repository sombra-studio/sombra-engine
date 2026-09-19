from importlib.resources import files

from pyglet.enums import (
    ComponentFormat, FramebufferAttachment, GeometryMode,
    TextureFilter, AddressMode
)
from pyglet.graphics.framebuffer import Framebuffer
from pyglet.graphics import Batch, ShaderGroup, Texture, Shader, ShaderProgram
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

    # Quad program
    quad_vs_src = files('sombra_engine.shaders').joinpath(
        'quad.vert'
    ).read_text()
    quad_vs = Shader(quad_vs_src, shader_type='vertex')
    quad_fs_str = files('sombra_engine.shaders').joinpath(
        'debug_shadow_map.frag'
    ).read_text()
    quad_fs = Shader(quad_fs_str, shader_type='fragment')
    quad_program: ShaderProgram = ShaderProgram(quad_vs, quad_fs)

    # Quad vertex list

    quad_shader_group = ShaderGroup(quad_program)
    quad_shader_group.set_texture(shadow_map)
    quad = quad_program.vertex_list(
        count=4,
        mode=GeometryMode.TRIANGLE_STRIP,
        position=(
            'f', (
                -1.0, 1.0, 0.0,
                -1.0, -1.0, 0.0,
                1.0, 1.0, 0.0,
                1.0, -1.0, 0.0
            )
        ),
        tex_coords=(
            'f', (
                0.0, 1.0,
                0.0, 0.0,
                1.0, 1.0,
                1.0, 0.0
            )
        )
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
        quad.draw(GeometryMode.TRIANGLE_STRIP)

    pyglet.app.run()



