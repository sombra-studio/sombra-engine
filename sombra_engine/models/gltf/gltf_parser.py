from enum import IntEnum
import io
from pygltflib import GLTF2, Accessor
from pyglet.image import Texture
import pyglet
import struct


class GLTFComponentType(IntEnum):
    BYTE = 5120
    UNSIGNED_BYTE = 5121
    SHORT = 5122
    UNSIGNED_SHORT = 5123
    UNSIGNED_INT = 5125
    FLOAT = 5126


GLTF_COMPONENTTYPE_SIZES = {
    GLTFComponentType.BYTE: 1,
    GLTFComponentType.UNSIGNED_BYTE: 1,
    GLTFComponentType.SHORT: 2,
    GLTFComponentType.UNSIGNED_SHORT: 2,
    GLTFComponentType.UNSIGNED_INT: 4,
    GLTFComponentType.FLOAT: 4
}

GLTF_ACCESSORTYPE_COUNTS = {
    "SCALAR": 1,
    "VEC2": 2,
    "VEC3": 3,
    "VEC4": 4,
    "MAT2": 4,
    "MAT3": 9,
    "MAT4": 16
}

GLTF_COMPONENT_UNPACK_FORMATS = {
    GLTFComponentType.BYTE: "b",
    GLTFComponentType.UNSIGNED_BYTE: "B",
    GLTFComponentType.SHORT: "h",
    GLTFComponentType.UNSIGNED_SHORT: "H",
    GLTFComponentType.UNSIGNED_INT: "I",
    GLTFComponentType.FLOAT: "f"
}


def get_dense_data(gltf: GLTF2, accessor: Accessor):
    buffer_view = gltf.bufferViews[accessor.bufferView]
    buffer = gltf.buffers[buffer_view.buffer]
    buffer_data = gltf.get_data_from_buffer_uri(buffer.uri)
    result = []
    elem_stride = GLTF_ACCESSORTYPE_COUNTS[accessor.type] * \
      GLTF_COMPONENTTYPE_SIZES[int(accessor.componentType)]
    for i in range(accessor.count):
        index = buffer_view.byteOffset + accessor.byteOffset + i * elem_stride
        base64_elem_data = buffer_data[index:index + elem_stride]
        format_count = GLTF_ACCESSORTYPE_COUNTS[accessor.type]
        format_type = GLTF_COMPONENT_UNPACK_FORMATS[accessor.componentType]
        elem_data = struct.unpack(
            f"<{format_type * format_count}",
            base64_elem_data
        )
        if len(elem_data) == 1:
            result.append(elem_data[0])
        else:
            result.append(elem_data)

    return result


def get_texture_from_gltf_image(img_gltf, gltf) -> Texture:
    fmt = img_gltf.mimeType.split('/')[-1]
    buffer_view = gltf.bufferViews[img_gltf.bufferView]
    offset = buffer_view.byteOffset
    length = buffer_view.byteLength
    buffer = gltf.buffers[buffer_view.buffer]
    image_data_bytes = gltf.get_data_from_buffer_uri(
        buffer.uri
    )[offset:offset + length]
    image_stream = io.BytesIO(image_data_bytes)
    tex = pyglet.image.load(
        f"image.{fmt}", file=image_stream
    ).get_texture()
    return tex


class GLTFParser:
    @staticmethod
    def parse(filename: str, scale: float = 1.0) -> dict:
        model_data = {
            "meshes_data": [],
            "materials_data": []
        }
        gltf = GLTF2().load(filename)

        # Parse mesh data
        for mesh in gltf.meshes:
            mesh_data = {
                "primitives": [],
                "name": mesh.name or "unnamed"
            }
            for primitive in mesh.primitives:
                indices = get_dense_data(gltf, gltf.accessors[primitive.indices])
                positions = get_dense_data(
                    gltf, gltf.accessors[primitive.attributes.POSITION]
                )
                normals = get_dense_data(
                    gltf, gltf.accessors[primitive.attributes.NORMAL]
                )
                tex_coords = get_dense_data(
                    gltf, gltf.accessors[primitive.attributes.TEXCOORD_0]
                )

                if scale != 1.0:
                    positions = [
                        tuple(
                            value * scale for value in pos
                        ) for pos in positions
                    ]

                primitive_data = {
                    "indices": indices,
                    "positions": positions,
                    "normals": normals,
                    "tex_coords": tex_coords,
                    "material": primitive.material,
                }

                mesh_data["primitives"].append(primitive_data)
            model_data["meshes_data"].append(mesh_data)

        # Parse materials data
        for material in gltf.materials:
            if material.pbrMetallicRoughness.baseColorTexture:
                diffuse_tex_gltf = gltf.textures[
                    material.pbrMetallicRoughness.baseColorTexture.index
                ]
                diffuse_img_gltf = gltf.images[diffuse_tex_gltf.source]
                diffuse_tex = get_texture_from_gltf_image(
                    diffuse_img_gltf, gltf
                )
            else:
                diffuse_tex = None

            if material.occlusionTexture:
                ambient_tex_gltf = gltf.textures[
                    material.occlusionTexture.index
                ]
                ambient_img_gltf = gltf.images[ambient_tex_gltf.source]
                ambient_tex = get_texture_from_gltf_image(
                    ambient_img_gltf, gltf
                )
            else:
                ambient_tex = None

            if material.normalTexture:
                normal_tex_gltf = gltf.textures[material.normalTexture.index]
                normal_img_gltf = gltf.images[normal_tex_gltf.source]
                normal_tex = get_texture_from_gltf_image(
                    normal_img_gltf, gltf
                )
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
                specular_tex_gltf = gltf.textures[
                    specular_data['specularTexture']['index']
                ]
                specular_img_gltf = gltf.images[specular_tex_gltf.source]
                specular_tex = get_texture_from_gltf_image(
                    specular_img_gltf, gltf
                )
            else:
                specular_tex = None

            material_data = {
                "name": material.name,
                "ambient_map": ambient_tex,
                "diffuse": material.pbrMetallicRoughness.baseColorFactor[:3],
                "diffuse_map": diffuse_tex,
                "specular_map": specular_tex,
                "specular_exponent": \
                    material.pbrMetallicRoughness.roughnessFactor,
                "normal_map": normal_tex,
            }
            model_data["materials_data"].append(material_data)

        return model_data
