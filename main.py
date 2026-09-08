from pyglet.math import Vec3
import pyglet


from sombra_engine.models import SkeletalMesh
from sombra_engine.models.gltf import GLTFLoader
from sombra_engine import App


pyglet.resource.path.append("./tests/data/")
pyglet.resource.reindex()

app = App(is_debug=True)


if __name__ == '__main__':
    scenes, skeletons, animations = GLTFLoader.load(
        filename='CesiumMan.glb',
        batch=app.batch
    )

    scene = scenes[0]
    mesh = scene.meshes[0]
    if isinstance(mesh, SkeletalMesh):
        if mesh.animations:
            animation_name = [k for k in mesh.animations.keys()][0]
            mesh.set_animation(animation_name)

    light_pos = Vec3(10.0, 8.0, 0.0)
    light_color = Vec3(1.0, 1.0, 1.0)
    scene.create_light(light_pos, light_color)
    app.set_scene(scene)
    app.run()
