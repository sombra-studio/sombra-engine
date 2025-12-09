from pyglet.math import Vec3
import pyglet


from sombra_engine.models.gltf import GLTFLoader
from sombra_engine import App, Scene


app = App(is_debug=True)
shader_program = None


def update(dt: float):
    global shader_program
    if shader_program is not None:
        if 'eye' in shader_program._uniforms:
            shader_program['eye'] = app.camera.position
        app.update(dt)



if __name__ == '__main__':
    batch = app.batch
    model = GLTFLoader.load(filename='tests/data/shoe_box.glb', batch=batch)

    scene = Scene()
    # scene.create_light(Vec3(100.0, 150.0, -7.0), Vec3(1.0, 1.0, 1.0))
    scene.create_light(Vec3(10.0, 8.0, 0.0), Vec3(1.0, 1.0, 1.0))

    program = model.meshes[0].program
    shader_program = program
    if 'light.position' in program._uniforms:
        program['light.position'] = scene.lights[0].position
    if 'light.color' in program._uniforms:
        program['light.color'] = scene.lights[0].color
    if 'eye' in program._uniforms:
        program['eye'] = app.camera.position

    app.add_model(model)

    pyglet.clock.schedule(update)
    app.run(0)
