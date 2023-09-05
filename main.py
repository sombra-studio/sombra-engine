from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Vec3
import pyglet


from sombra_engine.camera import FPSCamera
from sombra_engine.models.obj import OBJLoader
from sombra_engine.scene import Scene


window = pyglet.window.Window(caption="Sombra Engine")
camera = FPSCamera(
    window, position=Vec3(0.0, 0.0, -15.0), pitch=90, yaw=90
)
batch = pyglet.graphics.Batch()
model = None


@window.event
def on_draw():
    window.clear()
    batch.draw()
    # model.draw()


def main():
    global model
    with open('sombra_engine/shaders/default.vert') as f:
        vert_shader = Shader(f.read(), 'vertex')
    # with open('sombra_engine/shaders/lambert.frag') as f:
    with open('sombra_engine/shaders/solid_textured.frag') as f:
        frag_shader = Shader(f.read(), 'fragment')
    program = ShaderProgram(vert_shader, frag_shader)
    # scene = Scene()
    # scene.create_light(Vec3(100.0, 150.0, 7.0), Vec3(1.0))
    # light_ubo = program.uniform_blocks['Light'].create_ubo()
    # with light_ubo as light:
    #     light.position[:] = tuple(scene.lights[0].position)
    #     light.color[:] = tuple(scene.lights[0].color)
    model = OBJLoader.load(
        "tests/data/shoe_box2.obj", "House", program, batch=batch
        # "tests/data/yoda/yoda.obj", "Yoda", program, batch=batch
    )
    pyglet.app.run()


if __name__ == '__main__':
    main()
