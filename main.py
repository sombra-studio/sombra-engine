from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Mat4, Vec3
import pyglet


from sombra_engine.camera import FPSCamera
from sombra_engine.models.obj import OBJLoader
from sombra_engine.scene import Scene


window = pyglet.window.Window()
camera = FPSCamera(window)
batch = pyglet.graphics.Batch()
model = None


@window.event
def on_draw():
    window.clear()
    batch.draw()


def main():
    global model
    with open('sombra_engine/shaders/default.vert') as f:
        vert_shader = Shader(f.read(), 'vertex')
    with open('sombra_engine/shaders/lambert.frag') as f:
        frag_shader = Shader(f.read(), 'fragment')
    program = ShaderProgram(vert_shader, frag_shader)
    program['mv'] = Mat4()
    program['proj'] = Mat4()
    scene = Scene()
    scene.create_light(Vec3(100.0, 150.0, 7.0), Vec3(1.0))
    light_ubo = program.uniform_blocks['Light'].create_ubo()
    with light_ubo as light:
        light.position = scene.lights[0].position
        light.color = scene.lights[0].color
    model = OBJLoader.load(
        "tests/data/shoe_box2.obj", "House", program, batch=batch
    )
    print(model.name)
    pyglet.app.run()


if __name__ == '__main__':
    main()
