from pyglet.graphics.shader import Shader, ShaderProgram
import pyglet
from pyglet.math import Vec3

from sombra_engine.app import App
from sombra_engine.models.obj import OBJLoader
from sombra_engine.scene import Scene

app = App(is_debug=True)
model = None


def main():
    global model
    with open('sombra_engine/shaders/default.vert') as f:
        vs = Shader(f.read(), 'vertex')
    with open('sombra_engine/shaders/blinn.frag') as f:
        fs = Shader(f.read(), 'fragment')
    shader_program = ShaderProgram(vs, fs)
    model = OBJLoader.load(
        #"tests/data/shoe_box2.obj", "house", shader_program, batch
        filename="tests/data/cube.obj",
        name="house",
        program=shader_program,
        batch=app.batch
    )
    scene = Scene()
    scene.create_light(Vec3(100.0, 150.0, -7.0), Vec3(1.0, 1.0, 1.0))

    program = model.meshes[0].program
    program['light.position'] = scene.lights[0].position
    program['light.color'] = scene.lights[0].color

    program['eye'] = app.camera.position

    pyglet.app.run()


if __name__ == '__main__':
    main()
