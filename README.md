# Sombra Engine 

Small 3D Game Engine made in Python on top of the pyglet framework (work in 
progress).

The idea of this engine is:
- to be simple
- to run on lower end PCs 

## Planned features

- [x] UI library with shaders support (through [pudu-ui](https://github.com/sombra-studio/pudu-ui))
- [x] 3D models through glTF format (and limited support for OBJ)
- [x] OpenGL Renderer and GLSL shaders
- [x] Skeletal animations
- [ ] Shadows
- [ ] Rigid body physics
- [ ] Terrain rendering
- [ ] Foliage
- [ ] Particle systems
- [ ] Water
- [ ] Smoke, Fire, GFX
- [ ] Pathfinding


![screenshot](https://raw.githubusercontent.com/sombra-studio/sombra-engine/refs/heads/main/docs/screenshot.png)

## Installing

You can get it with pip:

`pip install sombra-engine`

or with uv:

`uv add sombra-engine`


## Example

Here is an example of loading a glTF file, setting an animation and creating a 
light

```py
from pyglet.math import Vec3
import pyglet


from sombra_engine.models import SkeletalMesh
from sombra_engine.models.gltf import GLTFLoader
from sombra_engine import App


pyglet.resource.path.append("./tests/data/")
pyglet.resource.reindex()

app = App(is_debug=True)


if __name__ == '__main__':
    scenes, skeletons, animations = GLTFLoader.load(
        filename='CesiumMan.glb',
        batch=app.batch
    )

    scene = scenes[0]
    mesh = scene.meshes[0]
    if isinstance(mesh, SkeletalMesh):
        if mesh.animations:
            animation_name = [k for k in mesh.animations.keys()][0]
            mesh.set_animation(animation_name)

    light_pos = Vec3(10.0, 8.0, 0.0)
    light_color = Vec3(1.0, 1.0, 1.0)
    scene.create_light(light_pos, light_color)
    app.set_scene(scene)
    app.run(0)
```

To run it locally you can download the repo and do:

`uv sync`

`uv run main.py`
