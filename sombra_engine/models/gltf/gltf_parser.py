from pyglet.model.codecs import gltf


def group_in_ms(l: list, m: int) -> list:
    return [l[i: i + m] for i in range(len(l) // m)]

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
            "materials_data": []
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
                            n = attribute.count
                            primitive_data['positions'] = group_in_3s(
                                attribute.array
                            )
                        case 'NORMAL':
                            n = attribute.count
                            primitive_data['normals'] = group_in_3s(
                                attribute.array
                            )
                        case 'TEXCOORD_0':
                            n = attribute.count
                            primitive_data['tex_coords'] = group_in_2s(
                                attribute.array
                            )

                if scale != 1.0:
                    positions = [
                        tuple(
                            value * scale for value in pos
                        ) for pos in positions
                    ]

                primitive_data['material'] = primitive.material

                mesh_data["primitives"].append(primitive_data)
            model_data["meshes_data"].append(mesh_data)

        # Parse materials data
        # for material in gltf.materials:
        #     if material.pbrMetallicRoughness.baseColorTexture:
        #         diffuse_tex_gltf = gltf.textures[
        #             material.pbrMetallicRoughness.baseColorTexture.index
        #         ]
        #         diffuse_img_gltf = gltf.images[diffuse_tex_gltf.source]
        #         diffuse_tex = get_texture_from_gltf_image(
        #             diffuse_img_gltf, gltf, root_path=root_path
        #         )
        #     else:
        #         diffuse_tex = None
        #
        #     if material.occlusionTexture:
        #         ambient_tex_gltf = gltf.textures[
        #             material.occlusionTexture.index
        #         ]
        #         ambient_img_gltf = gltf.images[ambient_tex_gltf.source]
        #         ambient_tex = get_texture_from_gltf_image(
        #             ambient_img_gltf, gltf, root_path=root_path
        #         )
        #     else:
        #         ambient_tex = None
        #
        #     if material.normalTexture:
        #         normal_tex_gltf = gltf.textures[material.normalTexture.index]
        #         normal_img_gltf = gltf.images[normal_tex_gltf.source]
        #         normal_tex = get_texture_from_gltf_image(
        #             normal_img_gltf, gltf, root_path=root_path
        #         )
        #     else:
        #         normal_tex = None
        #
        #     if (
        #         material.extensions and
        #         'KHR_materials_specular' in material.extensions and
        #         material.extensions['KHR_materials_specular'] and
        #         'specularTexture' in material.extensions[
        #             'KHR_materials_specular'
        #         ]
        #     ):
        #         specular_data = material.extensions['KHR_materials_specular']
        #         specular_tex_gltf = gltf.textures[
        #             specular_data['specularTexture']['index']
        #         ]
        #         specular_img_gltf = gltf.images[specular_tex_gltf.source]
        #         specular_tex = get_texture_from_gltf_image(
        #             specular_img_gltf, gltf, root_path=root_path
        #         )
        #     else:
        #         specular_tex = None
        #
        #     material_data = {
        #         "name": material.name,
        #         "ambient_map": ambient_tex,
        #         "diffuse": material.pbrMetallicRoughness.baseColorFactor[:3],
        #         "diffuse_map": diffuse_tex,
        #         "specular_map": specular_tex,
        #         "specular_exponent": \
        #             material.pbrMetallicRoughness.roughnessFactor,
        #         "normal_map": normal_tex,
        #     }
        #     model_data["materials_data"].append(material_data)

        return model_data
