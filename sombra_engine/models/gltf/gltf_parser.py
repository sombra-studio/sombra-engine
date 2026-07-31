from typing import Any
from pyglet.math import Mat4, Quaternion, Vec3
from pyglet.model.codecs import gltf


def group_in_ms(l: list, m: int) -> list:
    new_list = []
    for i in range(0, len(l), m):
        new_list.append(l[i:i + m])
    return new_list

def group_in_3s(l: list) -> list:
    return group_in_ms(l=l, m=3)


def group_in_2s(l: list) -> list:
    return group_in_ms(l=l, m=2)


def parse_material(
    material: gltf.Material, textures: list[gltf.Texture]
) -> dict[str, Any]:
    if material.base_color_texture:
        diffuse_tex_gltf = textures[
            material.base_color_texture['index']
        ]
        diffuse_tex = diffuse_tex_gltf.image.read().get_texture()
    else:
        diffuse_tex = None

    if material.occlusion_texture:
        ambient_tex_gltf = textures[
            material.occlusion_texture['index']
        ]
        ambient_tex = ambient_tex_gltf.image.read().get_texture()
    else:
        ambient_tex = None

    if material.normal_texture:
        normal_tex_gltf = textures[
            material.normal_texture['index']
        ]
        normal_tex = normal_tex_gltf.image.read().get_texture()
    else:
        normal_tex = None

    if (
            material.extensions and
            'KHR_materials_specular' in material.extensions and
            material.extensions['KHR_materials_specular'] and
            'specularTexture' in material.extensions[
        'KHR_materials_specular'
    ]
    ):
        specular_data = material.extensions['KHR_materials_specular']
        specular_tex_gltf = textures[
            specular_data['specularTexture']['index']
        ]
        specular_tex = specular_tex_gltf.image.read().get_texture()
    else:
        if material.metallic_roughness_texture:
            specular_tex_gltf = textures[
                material.metallic_roughness_texture['index']
            ]
            specular_tex = specular_tex_gltf.image.read().get_texture()
        else:
            specular_tex = None

    specular_exponent = 120
    material_data = {
        "name": material.name,
        "ambient_map": ambient_tex,
        "diffuse": material.base_color_factor[:3],
        "diffuse_map": diffuse_tex,
        "specular_map": specular_tex,
        "specular_exponent": specular_exponent,
        "normal_map": normal_tex,
    }
    return material_data


def parse_mesh(mesh: gltf.Mesh) -> dict[str, Any]:
    # Parse mesh data
    mesh_data = {
        "primitives": [],
        "name": mesh.name or "undefined"
    }
    for primitive in mesh.primitives:
        primitive_data = {}
        primitive_data['indices'] = primitive.indices
        for attribute in primitive.attributes:
            match attribute.name:
                case 'POSITION':
                    primitive_data['positions'] = group_in_3s(
                        attribute.array
                    )
                case 'NORMAL':
                    primitive_data['normals'] = group_in_3s(
                        attribute.array
                    )
                case 'TEXCOORD_0':
                    primitive_data['tex_coords'] = group_in_2s(
                        attribute.array
                    )
                case 'WEIGHTS_0':
                    primitive_data['weights'] = group_in_ms(
                        attribute.array, 4
                    )
                case 'JOINTS_0':
                    primitive_data['joints'] = group_in_ms(
                        attribute.array, 4
                    )

        primitive_data['material_name'] = primitive.material.name

        mesh_data["primitives"].append(primitive_data)
    return mesh_data


def parse_node(node: gltf.Node) -> dict[str, Any]:
    """
    Parse a node with its child nodes in the children attribute

    Args:
        node: A Node object from pyglet gltf decoder that will be parsed

    Returns:
        A dictionary with the node parsed for loading it later
    """
    node_data = {
        "name": node.name,
        "matrix": node.matrix,
        "translation": node.translation,
        "rotation": node.rotation,
        "scale": node.scale
    }
    if node.mesh:
        mesh_data = parse_mesh(node.mesh)
        node_data["mesh"] = mesh_data

    if node.children:
        node_data["children"] = []
        for child_node in node.children:
            child_data = parse_node(child_node)
            node_data["children"].append(child_data)

    return node_data

def parse_scene(scene: gltf.Scene) -> dict[str, Any]:
    scene_data = {
        "name": scene.name,
        "nodes": [parse_node(node) for node in scene.nodes]
    }
    return scene_data


class GLTFParser:
    @staticmethod
    def parse(filename: str) -> dict:
        parsed_data = {
            "scenes_data": [],
            "materials_data": {},
            "skins_data": [],
            "animations_data": []
        }
        data = gltf.load_gltf(filename)

        for scene in data.scenes:
            scene_data = parse_scene(scene)
            parsed_data["scenes_data"].append(scene_data)

        for material in data.materials:
            material_data = parse_material(material, data.textures)
            parsed_data["materials_data"][material.name] = material_data

        parsed_data["skins_data"] = data.skins
        parsed_data["animations_data"] = data.animations

        return parsed_data
