from pygltflib import GLTF2, Accessor
from enum import IntEnum
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
    bufferView = gltf.bufferViews[accessor.bufferView]
    buffer = gltf.buffers[bufferView.buffer]
    buffer_data = gltf.get_data_from_buffer_uri(buffer.uri)
    result = []
    elem_stride = GLTF_ACCESSORTYPE_COUNTS[accessor.type] * \
                  GLTF_COMPONENTTYPE_SIZES[int(accessor.componentType)]
    for i in range(accessor.count):
        index = bufferView.byteOffset + accessor.byteOffset + i * elem_stride
        base64_elem_data = buffer_data[index:index + elem_stride]
        elem_data = struct.unpack(
            f"<{GLTF_COMPONENT_UNPACK_FORMATS[accessor.componentType] * GLTF_ACCESSORTYPE_COUNTS[accessor.type]}",
            base64_elem_data
        )
        if len(elem_data) == 1:
            result.append(elem_data[0])
        else:
            result.append(elem_data)

    return result


class GLTFParser:
    def parse(self, filename: str) -> dict:
        model_data = {
            "meshes_data": [],
            "materials_data": []
        }
        gltf = GLTF2().load(filename)

        for mesh in gltf.meshes:
            mesh_data = {
                "primitives": []
            }
            for primitive in mesh.primitives:
                primitive_data = {}

                # indices = get_dense_data(gltf, gltf.accessors[primitive.indices])
                positions = get_dense_data(
                    gltf, gltf.accessors[primitive.attributes.POSITION]
                )

                primitive_data["positions"] = positions
                mesh_data["primitives"].append(primitive_data)
            model_data["meshes_data"].append(mesh_data)

        return model_data
