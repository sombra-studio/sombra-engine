from importlib.resources import files
from pyglet.math import Vec3
import pyglet

from sombra_engine.models import SkeletalMesh
from sombra_engine.models.gltf import GLTFLoader
from sombra_engine import App, Scene


pyglet.options['debug_gl_shaders'] = True

pyglet.resource.path.append("./tests/data/")
pyglet.resource.path.append("./tests/data/Avocado/")
pyglet.resource.reindex()

app = App(is_debug=True)

# vs_src = files('sombra_engine.shaders').joinpath(
#     'skeletal.vert'
#     # 'normals.vert'
# ).read_text()
# vert_shader = pyglet.graphics.Shader(vs_src, 'vertex')
#
# fs_src = files('sombra_engine.shaders').joinpath(
#     # 'blinn_barycentric.frag'
#     'normals_with_map.frag'
#     # 'normals.frag'
# ).read_text()
# frag_shader = pyglet.graphics.Shader(fs_src, 'fragment')
# shader_program = pyglet.graphics.ShaderProgram(vert_shader, frag_shader)
shader_program = None


def update(dt: float):
    global shader_program
    if shader_program is not None:
        if 'eye' in shader_program._uniforms:
            shader_program['eye'] = app.camera.position
    app.update(dt)



if __name__ == '__main__':
    batch = app.batch
    meshes, skeletons, animations = GLTFLoader.load(
        # filename='yoda/yoda.glb',
        # filename='CesiumMan.glb',
        # filename='BrainStem.glb',
        filename='zombie.glb',
        # filename='box.glb',
        # filename='plane.gltf',
        # program=shader_program,
        # filename='Avocado.gltf',
        batch=batch
    )

    mesh = meshes[0]
    if isinstance(mesh, SkeletalMesh):
        if mesh.animations:
            animation_name = [k for k in mesh.animations.keys()][0]
            mesh.set_animation(animation_name)

    scene = Scene()
    # scene.create_light(Vec3(100.0, 150.0, -7.0), Vec3(1.0, 1.0, 1.0))
    scene.create_light(Vec3(10.0, 8.0, 0.0), Vec3(1.0, 1.0, 1.0))
    scene.add_mesh(mesh)

    program = mesh.program
    if 'eye' in program._uniforms:
        program['eye'] = app.camera.position
    # shader_program = program
    app.set_scene(scene)

    pyglet.clock.schedule(update)
    app.run(0)
