import pyglet
from pyglet.math import Mat4, Vec3
from pyglet.window import Window


from sombra_engine.debug.gizmo import Gizmo


window = Window()
window.view = Mat4.look_at(
    position=Vec3(0.0, 0.0, -5.0),
    target=Vec3(0.0, 0.0, 0.0),
    up=Vec3(0.0, 1.0, 0.0)
)
window.projection = Mat4.perspective_projection(
    window.aspect_ratio, z_near=0.01, z_far=255, fov=60
)

gizmo = Gizmo()


@window.event
def on_draw():
    window.clear()
    gizmo.draw()


def main():
    pyglet.app.run()


if __name__ == '__main__':
    main()
