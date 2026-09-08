import pyglet
from pyglet.math import Vec3

from sombra_engine import App, Scene
from sombra_engine.models import Mesh
from sombra_engine.models.obj import OBJLoader


if __name__ == '__main__':
    pyglet.resource.path.append("./tests/data/")
    pyglet.resource.reindex()
    app = App()
    # Create mesh and plane
    plane_scene = OBJLoader.load('plane.obj', batch=app.batch)
    scene = Scene()
    if plane_scene.meshes and (plane_scene.meshes[0], Mesh):
        plane_mesh = plane_scene.meshes[0]
        scene.add_mesh(plane_mesh)

    # Add light
    light_pos = Vec3(10.0, 8.0, 0.0)
    light_color = Vec3(1.0, 1.0, 1.0)
    scene.create_light(light_pos, light_color)

    # Create mesh and plane using the shadow map program

    app.set_scene(scene)
    app.run()
