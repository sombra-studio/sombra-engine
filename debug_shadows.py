from importlib.resources import files

import pyglet
from pyglet.graphics import Batch, Shader, ShaderProgram
from pyglet.math import Mat4, Vec3

from sombra_engine import App, Scene
from sombra_engine.models import Mesh
from sombra_engine.models.gltf import GLTFLoader
from sombra_engine.models.obj import OBJLoader


if __name__ == '__main__':
    pyglet.resource.path.append("./tests/data/")
    pyglet.resource.reindex()
    app = App(update_rate=0.0 ,vsync=False, is_debug=True)
    # Create mesh and plane
    plane_scene = OBJLoader.load('plane.obj', batch=app.batch)
    scene = Scene()
    if plane_scene.meshes and (plane_scene.meshes[0], Mesh):
        plane_mesh = plane_scene.meshes[0]
        plane_mesh.scale(Vec3(5, 5, 5))
        scene.add_mesh(plane_mesh)
    else:
        raise Exception("Plane not found")

    gltf_scenes, _, __ = GLTFLoader.load(
        # filename='zombie.glb',
        # filename='CesiumMan.glb',
        filename='box.glb',
        batch=app.batch
    )
    if (
        gltf_scenes and gltf_scenes[0].meshes and
        isinstance(gltf_scenes[0].meshes[0], Mesh)
    ):
        mesh = gltf_scenes[0].meshes[0]
        scene.add_mesh(mesh)
    else:
        raise Exception("Mesh not found")

    # Add light
    light_pos = Vec3(10.0, 8.0, 0.0)
    light_color = Vec3(1.0, 1.0, 1.0)
    scene.create_light(light_pos, light_color)

    # Create Shadow Map
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

    # Create light camera
    light_projection = Mat4.orthogonal_projection(
        left=-10.0, right=10.0, bottom=-10.0, top=10.0, z_near=1.0, z_far=8.0
    )
    light_view = Mat4.look_at(
        position=light_pos,
        target=Vec3(),
        up=Vec3(0.0, 1.0, 0.0)
    )
    light_transform = light_projection @ light_view

    # We need to pass the light transform uniform to the Material group

    # Create mesh and plane using the shadow map program
    shadows_batch = Batch()
    for vg_name, vg in mesh.vertex_groups.items():
        position_list = mesh.get_position_list_for_vertex_group(vg_name)
        shadow_map_program.vertex_list(
            count=len(vg.triangles),
            mode=mesh.mode,
            batch=shadows_batch,
            # TODO add shadow groups
            position=('f', position_list)
        )
    for vg_name, vg in plane_mesh.vertex_groups.items():
        position_list = plane_mesh.get_position_list_for_vertex_group(vg_name)
        shadow_map_program.vertex_list(
            count=len(vg.triangles),
            mode=plane_mesh.mode,
            batch=shadows_batch,
            position=('f', position_list)
        )

    # We need a custom app class that uses a different draw function

    app.set_scene(scene)
    app.run()
