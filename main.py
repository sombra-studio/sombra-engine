from pyglet.graphics import Group
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Vec3
from pyglet.window import key
import pyglet


from sombra_engine.camera import FPSCamera
from sombra_engine.models import Wireframe
from sombra_engine.models.obj import OBJLoader
from sombra_engine.scene import Scene


window = pyglet.window.Window(caption="Sombra Engine")
camera = FPSCamera(
    window, position=Vec3(0.0, 0.0, -15.0), pitch=90, yaw=90
)
batch = pyglet.graphics.Batch()
model = None
wf = None


# @window.event
# def on_key_press(symbol, mod):
#     if symbol == key.P:
#         pyglet.image.get_buffer_manager().get_color_buffer().save(
#             'screenshot.png'
#         )


@window.event
def on_draw():
    window.clear()
    pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
    batch.draw()


def main():
    global model, wf
    with open('sombra_engine/shaders/default.vert') as f:
        vert_shader = Shader(f.read(), 'vertex')
    with open('sombra_engine/shaders/lambert.frag') as f:
    # with open('sombra_engine/shaders/solid.frag') as f:
    # with open('sombra_engine/shaders/normals.frag') as f:
        frag_shader = Shader(f.read(), 'fragment')
    program = ShaderProgram(vert_shader, frag_shader)

    scene = Scene()
    scene.create_light(Vec3(100.0, 150.0, 7.0), Vec3(1.0, 1.0, 1.0))
    program.uniforms['light.position'].set(scene.lights[0].position)
    program.uniforms['light.color'].set(scene.lights[0].color)

    # model_group = Group()
    # model_group.visible = False
    model = OBJLoader.load(
        "tests/data/shoe_box2.obj", "House", program, batch=batch,
        # group=model_group
        # "tests/data/yoda/yoda.obj", "Yoda", program, batch=batch
    )
    # wf = Wireframe(model.meshes[0], vert_shader, batch)
    pyglet.app.run()


if __name__ == '__main__':
    main()
