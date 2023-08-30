from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Vec3
import pyglet


from sombra_engine.camera import FPSCamera
from sombra_engine.models.obj import OBJLoader


window = pyglet.window.Window()
camera = FPSCamera(
    window, position=Vec3(0.0, 0.0, -15.0), pitch=90, yaw=90
)
batch = pyglet.graphics.Batch()
model = None


@window.event
def on_draw():
    window.clear()
    batch.draw()


def main():
    global model
    with open('sombra_engine/shaders/default.vert') as f:
        vs = Shader(f.read(), 'vertex')
    with open('sombra_engine/shaders/solid.frag') as f:
        fs = Shader(f.read(), 'fragment')
    shader_program = ShaderProgram(vs, fs)
    model = OBJLoader.load(
        "tests/data/shoe_box2.obj", "house", shader_program, batch
    )
    pyglet.app.run()


if __name__ == '__main__':
    main()
