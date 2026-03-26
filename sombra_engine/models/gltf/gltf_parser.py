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


class GLTFParser:
    @staticmethod
    def parse(filename: str, scale: float = 1.0) -> dict:
        idx = filename[::-1].find('/')
        root_path = filename[:-idx]
        model_data = {
            "meshes_data": [],
            "materials_data": {}
        }
        scene = gltf.load_gltf(filename)

        # Parse mesh data
        for mesh in scene.meshes:
            mesh_data = {
                "primitives": [],
                "name": mesh.name or "unnamed"
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

                if scale != 1.0:
                    primitive_data['positions'] = [
                        tuple(
                            value * scale for value in pos
                        ) for pos in primitive_data['positions']
                    ]

                primitive_data['material_name'] = primitive.material.name

                mesh_data["primitives"].append(primitive_data)
            model_data["meshes_data"].append(mesh_data)

        # Parse materials data
        for material in scene.materials:
            if material.base_color_texture:
                diffuse_tex_gltf = scene.textures[
                    material.base_color_texture['index']
                ]
                diffuse_tex = diffuse_tex_gltf.image.read().get_texture()
            else:
                diffuse_tex = None

            if material.occlusion_texture:
                ambient_tex_gltf = scene.textures[
                    material.occlusion_texture['index']
                ]
                ambient_tex = ambient_tex_gltf.image.read().get_texture()
            else:
                ambient_tex = None

            if material.normal_texture:
                normal_tex_gltf = scene.textures[
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
                specular_tex_gltf = scene.textures[
                    specular_data['specularTexture']['index']
                ]
                specular_tex = specular_tex_gltf.image.read().get_texture()
            else:
                if material.metallic_roughness_texture:
                    specular_tex_gltf = scene.textures[
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
            model_data["materials_data"][material.name] = material_data

        return model_data
