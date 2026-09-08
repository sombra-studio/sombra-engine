from collections.abc import Callable
from pyglet.graphics import Texture
import pyglet


from .mtl_parser import MTLParser
from sombra_engine.primitives import Material
from sombra_engine import utils


def set_map(data: dict, map_name: str, default_tex_func: Callable[[], Texture]):
    if map_name in data and data[map_name]:
        img = pyglet.resource.image(data[map_name])
        data[map_name] = img.get_texture()
        if map_name == 'bump_map':
            data["has_bump_map"] = True
        elif map_name == 'specular_map':
            data["has_specular_map"] = True
    else:
        data[map_name] = default_tex_func()


class MTLLoader:
    @staticmethod
    def load(filename: str) -> dict[str, Material]:
        materials = {}
        mtl_parser = MTLParser()
        mtl_parser.parse(filename)
        material_id = 1
        for name, data in mtl_parser.materials.items():
            set_map(
                data,
                map_name='ambient_map',
                default_tex_func=utils.create_white_tex
            )
            set_map(
                data,
                map_name='diffuse_map',
                default_tex_func=utils.create_white_tex
            )
            set_map(
                data,
                map_name='specular_map',
                default_tex_func=utils.create_black_tex
            )
            set_map(
                data,
                map_name='bump_map',
                default_tex_func=utils.create_black_tex
            )

            materials[name] = Material(material_id=material_id, **data)
            material_id += 1
        return materials
