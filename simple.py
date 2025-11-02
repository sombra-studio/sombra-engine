from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.graphics import Group
import pyglet
from pyglet.math import Vec3

from sombra_engine.app import App
from sombra_engine.models.obj import OBJLoader
from sombra_engine.scene import Scene

app = App(is_debug=True)
model = None
shader_program = None


def update(dt):
    global shader_program
    if 'eye' in shader_program._uniforms:
        shader_program['eye'] = app.camera.position
    app.update(dt)


def main():
    global model, shader_program
    with open('sombra_engine/shaders/default.vert') as f:
        vs = Shader(f.read(), 'vertex')
    with open('sombra_engine/shaders/blinn_barycentric.frag') as f:
        fs = Shader(f.read(), 'fragment')
    shader_program = ShaderProgram(vs, fs)
    model_group = Group()
    model = OBJLoader.load(
        # filename="tests/data/cube.obj",
        filename="tests/data/yoda/yoda.obj",
        # filename="tests/data/shoe_box2.obj",
        name="model",
        program=shader_program,
        group=model_group,
        batch=app.batch
    )
    scene = Scene()
    # scene.create_light(Vec3(100.0, 150.0, -7.0), Vec3(1.0, 1.0, 1.0))
    scene.create_light(Vec3(10.0, 8.0, 0.0), Vec3(1.0, 1.0, 1.0))

    program = model.meshes[0].program
    if 'light.position' in program._uniforms:
        program['light.position'] = scene.lights[0].position
    if 'light.color' in program._uniforms:
        program['light.color'] = scene.lights[0].color
    if 'eye' in program._uniforms:
        program['eye'] = app.camera.position

    app.add_model(model)

    pyglet.clock.schedule(update)
    pyglet.app.run(0)


if __name__ == '__main__':
    main()
