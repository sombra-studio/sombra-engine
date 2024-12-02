import pyglet
from pyglet.math import Vec3
from pyglet.window import Window


from sombra_engine.camera import FPSCamera
from sombra_engine.debug.gizmo import Gizmo


window = Window()
camera = FPSCamera(
    window, position=Vec3(0.85, 0.8, -2.15), pitch=102.0, yaw=110.0
)
camera.speed = 1.0
batch = pyglet.graphics.Batch()
gizmo = Gizmo(batch=batch)


@window.event
def on_draw():
    window.clear()
    batch.draw()


def main():
    pyglet.app.run()


if __name__ == '__main__':
    main()
