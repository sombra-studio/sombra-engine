from collections.abc import Callable
from pyglet.enums import GeometryMode
from pyglet.graphics import Batch, Group, ShaderProgram, Texture
from pyglet.math import Mat4, Quaternion, Vec2, Vec3, Vec4
from pyglet.model.codecs.gltf import Node, Skin

from sombra_engine.animations import Animation, Bone, Skeleton
from sombra_engine.models import Model, SkeletalMesh
from sombra_engine.primitives import (
    Material, SceneObject, Transform,
    Triangle, Vertex, VertexGroup
)
from sombra_engine.models.gltf import GLTFParser
from sombra_engine import utils


def get_triangles_from_data(data: dict) -> list[Triangle]:
    triangles = []
    num_vertices = len(data["indices"])
    for tri_num in range(num_vertices // 3):
        new_vertices = []
        for i in range(3):
            index = data["indices"][tri_num * 3 + i]
            position: Vec3 = Vec3(*data["positions"][index])
            normal: Vec3 = Vec3(*data["normals"][index])
            # Flip Vertical texture coordinates!
            if data.get("tex_coords"):
                uvs: list[float] = data["tex_coords"][index]
            else:
                uvs = [0.0, 0.0]
            v_coord = int(uvs[1]) + (1 - (uvs[1] % 1))
            tex_coords: Vec2 = Vec2(uvs[0], v_coord)

            if "joints" in data:
                bones_ids: tuple = tuple(data["joints"][index][:4])
            else:
                bones_ids: tuple = (0, 0, 0, 0)

            if "weights" in data:
                weights: Vec4 = Vec4(*data["weights"][index])
            else:
                weights: Vec4 = Vec4(1.0)

            vertex = Vertex(
                position=position,
                normal=normal,
                tex_coords=tex_coords,
                bones_ids=bones_ids[:4],
                weights=weights
            )
            new_vertices.append(vertex)
        new_triangle = Triangle(new_vertices)
        triangles.append(new_triangle)
    return triangles


def set_map(data: dict, map_name: str, default_tex_func: Callable[[], Texture]):
    if map_name in data and data[map_name]:
        if map_name == 'bump_map':
            data["has_bump_map"] = True
        elif map_name == 'specular_map':
            data["has_specular_map"] = True
        elif map_name == 'normal_map':
            data["has_normal_map"] = True
    else:
        data[map_name] = default_tex_func()


def get_node_local_transform(node: Node) -> Mat4:
    if node.translation:
        t = Mat4.from_translation(Vec3(*node.translation))
    else:
        t = Mat4()

    if node.rotation:
        r = Quaternion(node.rotation[3], *node.rotation[:3]).to_mat4()
    else:
        r = Mat4()

    if node.scale:
        s = Mat4.from_scale(Vec3(*node.scale))
    else:
        s = Mat4()


    local_transform = t @ r @ s
    return local_transform


def create_skeleton(skin: Skin) -> Skeleton:
    bones: list[Bone] = []

    for i, joint in enumerate(skin.joints):
        offset = i * 16
        local_transform = get_node_local_transform(joint)
        bone = Bone(
            idx=joint.index,
            bone_idx=i,
            name=joint.name,
            local_bind_transform=local_transform,
            inverse_bind_transform=Mat4(
                *skin.inverse_bind_matrices[offset:offset+16]
            )
        )
        bones.append(bone)

    # Set children
    for i, joint in enumerate(skin.joints):
        if joint.children:
            for child_node in joint.children:
                child_bone = [
                    bone for bone in bones if bone.idx == child_node.index
                ][0]
                bones[i].children.append(child_bone)

    root_idx = skin.skeleton_index
    if not skin.skeleton_index:
        # If the skin doesn't use the skeleton property assume first joint is
        # the root
        root_idx = 0

    skeleton = Skeleton(bones=bones, root_idx=root_idx)
    return skeleton


def load_animations(data: dict) -> dict[str, Animation]:
    animations = {}
    for anim_data in data:
        animation = Animation(anim_data)
        animations[anim_data.name]  = animation

    return animations


class GLTFLoader:
    @staticmethod
    def load(
        filename: str,
        name: str | None = None,
        scale: float = 1.0,
        mode: GeometryMode = GeometryMode.TRIANGLES,
        batch: Batch | None = None,
        group: Group | None = None,
        program: ShaderProgram | None = None,
        transform: Transform = Transform(),
        parent: SceneObject | None = None
    ) -> Model:


        # We need a dict with data
        # meshes_data has a shape like this:
        # {
        #     "meshes_data": [
        #       {
        #           "indices": [1, 2, 3, ...],
        #           "positions": [(132.4, 427.2, 12.3), (...), ...]
        #       }
        #     ],
        #     "materials_data": {
        #       "Wood": {
        #           "name": "Wood",
        #           "diffuse_color": (1.0, 1.0, 1.0, 1.0)
        #       },
        #       "Stone": {
        #           ....
        #       }
        #     }
        # }
        parsed_data = GLTFParser.parse(filename)
        transform.scale *= Vec3(scale, scale, scale)
        meshes_data = {}

        # Create materials
        materials_dict = {}
        idx = 1
        for name, material_data in parsed_data["materials_data"].items():
            set_map(
                material_data,
                map_name='ambient_map',
                default_tex_func=utils.create_white_tex
            )
            set_map(
                material_data,
                map_name='diffuse_map',
                default_tex_func=utils.create_white_tex
            )
            set_map(
                material_data,
                map_name='specular_map',
                default_tex_func=utils.create_black_tex
            )
            set_map(
                material_data,
                map_name='normal_map',
                default_tex_func=utils.create_blue_tex
            )

            material = Material(material_id=idx, **material_data)
            idx += 1
            materials_dict[name] = material

        # Create vertex group data
        for data in parsed_data["meshes_data"]:
            name = data["name"]
            vertex_groups_data = {}
            for i, primitive_data in enumerate(data["primitives"]):
                triangles = get_triangles_from_data(primitive_data)
                vg_name = str(i)
                vg_data = {
                    "name": vg_name,
                    "triangles": triangles,
                    "material": materials_dict[primitive_data['material_name']]
                }
                vertex_groups_data[vg_name] = vg_data

            # Create bones
            if data.get('skins'):
                skeleton = create_skeleton(data['skins'][0])
            else:
                skeleton = None
            # iterate bones hierarchy

            # Create animations
            if data.get('animations'):
                animations = load_animations(data['animations'])
            else:
                animations = []

            meshes_data[name] = {
                'vertex_groups': vertex_groups_data,
                'skeleton': skeleton,
                'animations': animations
            }
        meshes = []

        for mesh_name, mesh_data in meshes_data.items():
            # Create vertex groups
            vertex_groups: dict[str, VertexGroup] = {}
            materials: dict[str, Material] = {}
            for vg_name, vg_data in mesh_data['vertex_groups'].items():
                material = vg_data['material']
                vertex_groups[vg_name] = VertexGroup(
                    vg_name, vg_data['triangles'], material
                )
                materials[material.name] = material

            mesh = SkeletalMesh(
                name=mesh_name,
                vertex_groups=vertex_groups,
                materials=materials,
                skeleton=mesh_data['skeleton'],
                animations=mesh_data['animations'],
                mode=mode,
                batch=batch,
                group=group,
                program=program,
                transform=transform,
                parent=parent
            )
            meshes.append(mesh)

        model = Model(
            name=name,
            meshes=meshes,
            transform=transform,
            parent=parent
        )
        return model
