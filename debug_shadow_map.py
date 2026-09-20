from importlib.resources import files
from pyglet.enums import (
    ComponentFormat, FramebufferAttachment, GeometryMode,
    TextureFilter, AddressMode
)
from pyglet.graphics.api.gl.gl import (
    GL_CULL_FACE, GL_DEPTH_TEST, GL_LESS, GL_NONE, glClearColor, glDepthFunc,
    glDisable, glDrawBuffer, glEnable, glViewport, glReadBuffer, glClear,
    GL_DEPTH_BUFFER_BIT
)
from pyglet.graphics.framebuffer import Framebuffer
from pyglet.graphics import Batch, ShaderGroup, Texture, Shader, ShaderProgram
from pyglet.graphics.vertexdomain import VertexList
from pyglet.math import Mat4, Vec3
import pyglet


from sombra_engine.graphics.shadow_group import ShadowGroup
from sombra_engine.models import Mesh
from sombra_engine.models.gltf import GLTFLoader
from sombra_engine.models.obj import OBJLoader


DEPTH_MAP_WIDTH = 1024
DEPTH_MAP_HEIGHT = 1024


if __name__ == '__main__':
    pyglet.resource.path.append("./tests/data/")
    pyglet.resource.reindex()

    window = pyglet.window.Window(
        width=DEPTH_MAP_WIDTH, height=DEPTH_MAP_HEIGHT
    )
    box_scenes, _, __ = GLTFLoader.load('box.glb')
    plane_scene = OBJLoader.load('plane.obj')

    if (
        box_scenes and box_scenes[0].meshes and
        isinstance(box_scenes[0].meshes[0], Mesh)
    ):
        mesh = box_scenes[0].meshes[0]
    else:
        raise Exception("Mesh not found")

    if plane_scene.meshes and isinstance(plane_scene.meshes[0], Mesh):
        plane_mesh = plane_scene.meshes[0]
        plane_mesh.scale(Vec3(5, 5, 5))
    else:
        raise Exception("Plane not found")

    # Add light
    light_pos = Vec3(-2.0, 4.0, -1.0)
    # Create light camera
    light_projection = Mat4.orthogonal_projection(
        left=-10.0, right=10.0, bottom=-10.0, top=10.0, z_near=1.0, z_far=20.0
    )
    light_view = Mat4.look_at(
        position=light_pos,
        target=Vec3(),
        up=Vec3(0.0, 1.0, 0.0)
    )
    light_transform = light_projection @ light_view

    # Depth Map Texture
    depth_framebuffer: Framebuffer = Framebuffer()
    depth_map = Texture.create(
        width=DEPTH_MAP_WIDTH,
        height=DEPTH_MAP_HEIGHT,
        internal_format=ComponentFormat.D,
        internal_format_size=16,
        filters=TextureFilter.NEAREST,
        address_mode=AddressMode.CLAMP_TO_BORDER
    )
    depth_framebuffer.attach_texture(
        depth_map,
        attachment=FramebufferAttachment.DEPTH
    )
    depth_framebuffer.bind()
    glDrawBuffer(GL_NONE)
    glReadBuffer(GL_NONE)
    depth_framebuffer.unbind()

    # Depth Map Program
    # Create program
    depth_map_vs_str = files('sombra_engine.shaders').joinpath(
        'depth.vert'
    ).read_text()
    depth_map_vs = Shader(depth_map_vs_str, shader_type='vertex')
    depth_map_fs_str = files('sombra_engine.shaders').joinpath(
        'empty.frag'
    ).read_text()
    depth_map_fs = Shader(depth_map_fs_str, shader_type='fragment')
    depth_map_program: ShaderProgram = ShaderProgram(
        depth_map_vs, depth_map_fs
    )

    # Cloned geometry for shadows
    # Mesh
    vlists: list[VertexList] = []
    if mesh.vertex_groups is None:
        raise Exception("Empty mesh")
    for vg_name, vg in mesh.vertex_groups.items():
        position_list = mesh.get_position_list_for_vertex_group(vg_name)
        shadow_group = ShadowGroup(
            light_transform, depth_map_program, mesh.matrix
        )
        vl = depth_map_program.vertex_list(
            count=len(vg.triangles) * 3,
            mode=mesh.mode,
            group=shadow_group,
            position=('f', position_list)
        )
        vlists.append(vl)
    # Plane
    if plane_mesh.vertex_groups is None:
        raise Exception("Empty plane")
    for vg_name, vg in plane_mesh.vertex_groups.items():
        position_list = plane_mesh.get_position_list_for_vertex_group(vg_name)
        shadow_group = ShadowGroup(
            light_transform, depth_map_program, plane_mesh.matrix
        )
        vl = depth_map_program.vertex_list(
            count=len(vg.triangles) * 3,
            mode=plane_mesh.mode,
            group=shadow_group,
            position=('f', position_list)
        )
        vlists.append(vl)

    # Debug Quad program
    quad_vs_src = files('sombra_engine.shaders').joinpath(
        'quad.vert'
    ).read_text()
    quad_vs = Shader(quad_vs_src, shader_type='vertex')
    quad_fs_str = files('sombra_engine.shaders').joinpath(
        'debug_depth_map.frag'
    ).read_text()
    quad_fs = Shader(quad_fs_str, shader_type='fragment')
    quad_program: ShaderProgram = ShaderProgram(quad_vs, quad_fs)

    # Quad vertex list
    quad_shader_group = ShaderGroup(quad_program)
    quad_shader_group.set_texture(depth_map)
    quad = quad_program.vertex_list(
        count=4,
        mode=GeometryMode.TRIANGLE_STRIP,
        group=quad_shader_group,
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
        # glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        # Shadow pass
        glViewport(0, 0, DEPTH_MAP_WIDTH, DEPTH_MAP_HEIGHT)
        depth_framebuffer.bind()
        depth_map.bind()
        glClear(GL_DEPTH_BUFFER_BIT)
        for vl in vlists:
            vl.draw(GeometryMode.TRIANGLES)
        depth_framebuffer.unbind()
        # with shadows_batch.draw_with_options() as options:
        #     options.framebuffer = shadows_framebuffer
        #     options.viewport = (0, 0, SHADOW_MAP_WIDTH, SHADOW_MAP_HEIGHT)

        # Normal pass
        quad.draw(GeometryMode.TRIANGLE_STRIP)

    pyglet.app.run()
