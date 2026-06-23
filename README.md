# sombra-engine 

Game Engine made in Python on top of the pyglet framework (work in progress).

## Planned features

- 3D models through glTF format (and limited support for OBJ)
- OpenGL Renderer and GLSL shaders
- Skeletal animations
- Shadows
- Pathfinding
- Rigid body physics
- Particle systems
- Terrain rendering
- UI library with shaders support (through [pudu-ui](https://github.com/sombra-studio/pudu-ui))

![screenshot](https://raw.githubusercontent.com/sombra-studio/sombra-engine/refs/heads/main/docs/screenshot.png)

You can get the OBJ model of Yoda from [here](https://graphics.cs.utah.edu/courses/cs6610/spring2022/prj04/yoda.zip)

## Installing

You can get it with pip:

`pip install sombra-engine`


## Example

```py
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
    model = OBJLoader.load(
        filename="yoda.obj",
        name="model",
        batch=app.batch
    )
    scene = Scene()
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
    pyglet.app.run(0)


if __name__ == '__main__':
    main()

```
