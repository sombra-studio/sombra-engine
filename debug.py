from pyglet.math import Vec3
import pyglet

from sombra_engine.models import SkeletalMesh
from sombra_engine.models.gltf import GLTFLoader
from sombra_engine import App


pyglet.options['debug_gl_shaders'] = True

pyglet.resource.path.append("./tests/data/")
pyglet.resource.path.append("./tests/data/Avocado/")
pyglet.resource.reindex()

app = App(is_debug=True)


if __name__ == '__main__':
    batch = app.batch
    scenes, skeletons, animations = GLTFLoader.load(
        # filename='yoda/yoda.glb',
        # filename='CesiumMan.glb',
        # filename='BrainStem.glb',
        filename='zombie_walk.glb',
        # filename='box.glb',
        # filename='shoe_box.glb',
        # filename='plane.gltf',
        # program=shader_program,
        # filename='Avocado.gltf',
        batch=batch
    )

    scene = scenes[0]
    mesh = scene.meshes[0]
    if isinstance(mesh, SkeletalMesh):
        if mesh.animations:
            animation_name = [k for k in mesh.animations.keys()][0]
            mesh.set_animation(animation_name)

    scene.create_light(Vec3(10.0, 8.0, 0.0), Vec3(1.0, 1.0, 1.0))
    app.set_scene(scene)
    app.run(0)
