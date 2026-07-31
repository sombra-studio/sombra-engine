from collections.abc import Callable
import math
from typing import Any

from pyglet.enums import GeometryMode
from pyglet.graphics import Batch, Group, ShaderProgram, Texture
from pyglet.math import Mat4, Quaternion, Vec2, Vec3, Vec4
from pyglet.model.codecs.gltf import Skin

from sombra_engine.animations import Animation, Bone, Skeleton
from sombra_engine.models import Mesh, SkeletalMesh
from sombra_engine.primitives import (
    Material, SceneObject, Transform,
    Triangle, Vertex, VertexGroup
)
from sombra_engine.models.gltf import GLTFParser
from sombra_engine import Scene, utils


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
    """
    Set a texture mapping some material property, like "normal_map",
    "diffuse_map", etc.

    Args:
        data: A dictionary with the material properties
        map_name: The name of the texture map
        default_tex_func: A reference to the function that creates the
            default texture in case the map is not found in the data
    """
    if map_name in data and data[map_name]:
        if map_name == 'bump_map':
            data["has_bump_map"] = True
        elif map_name == 'specular_map':
            data["has_specular_map"] = True
        elif map_name == 'normal_map':
            data["has_normal_map"] = True
    else:
        data[map_name] = default_tex_func()


def create_material(material_data: dict, idx: int) -> Material:
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
    return material


def create_skeleton(skin: Skin) -> Skeleton:
    bones: list[Bone] = []

    for i, joint in enumerate(skin.joints):
        local_transform = joint.local_transform
        bone = Bone(
            idx=joint.index,
            bone_idx=i,
            name=joint.name,
            local_bind_transform=local_transform,
            inverse_bind_transform=skin.inverse_bind_matrices[i]
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

    if skin.skeleton_index is None:
        # If the skin doesn't use the skeleton property assume first joint is
        # the root
        if bones:
            root = bones[0]
        else:
            raise Exception(
                f"Can't create skeleton from empty skin: {skin.joints}"
            )
    else:
        root_idx = skin.skeleton_index
        root = None
        for bone in bones:
            if bone.idx == root_idx:
                root = bone
        if root is None:
            # In this case the root is a simple node
            joint = skin.skeleton
            if joint:
                local_transform = joint.local_transform
            else:
                local_transform = Mat4()
            root = Bone(
                idx=joint.index,
                bone_idx=-1,
                name=joint.name,
                local_bind_transform=local_transform,
                inverse_bind_transform=Mat4()
            )
            # Add children
            for child_node in joint.children:
                child_bone = [
                    bone for bone in bones if bone.idx == child_node.index
                ][0]
                root.children.append(child_bone)

    skeleton = Skeleton(bones=bones, root=root)
    return skeleton


def load_animations(data: dict) -> dict[str, Animation]:
    animations = {}
    for anim_data in data:
        animation = Animation(anim_data)
        animations[anim_data.name]  = animation

    return animations


def get_euler_angles(q: Quaternion):
    """
    Extracts Euler angles (rot_x, rot_y, rot_z) in radians from a pyglet Quaternion.
    """
    # rot_x / Roll (X-axis rotation)
    sinr_cosp = 2.0 * (q.w * q.x + q.y * q.z)
    cosr_cosp = 1.0 - 2.0 * (q.x * q.x + q.y * q.y)
    rot_x = math.atan2(sinr_cosp, cosr_cosp)

    # rot_y / Pitch (Y-axis rotation)
    sinp = 2.0 * (q.w * q.y - q.z * q.x)
    if abs(sinp) >= 1.0:
        # Use exactly 90 degrees (pi/2) if the math drifts slightly out of bounds
        rot_y = math.copysign(math.pi / 2, sinp)
    else:
        rot_y = math.asin(sinp)

    # rot_z / Yaw (Z-axis rotation)
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    rot_z = math.atan2(siny_cosp, cosy_cosp)

    return rot_x, rot_y, rot_z


def create_object(
    node_data: dict[str, Any],
    materials: dict[str, Material],
    skeleton: Skeleton | None,
    animations: dict[str, Animation],
    scene: Scene,
    mode: GeometryMode = GeometryMode.TRIANGLES,
    batch: Batch | None = None,
    group: Group | None = None,
    program: ShaderProgram | None = None,
    parent: SceneObject | None = None
) -> SceneObject:
    transform = get_transform_from_node_data(node_data)
    matrix = Mat4(*node_data["matrix"]) if node_data["matrix"] else Mat4()

    scene_obj = SceneObject(
        name=node_data["name"],
        transform=transform,
        matrix=matrix,
        parent=parent
    )

    if node_data.get("mesh"):
        mesh_data = node_data["mesh"]
        vertex_groups_data = {}
        for i, primitive_data in enumerate(mesh_data["primitives"]):
            triangles = get_triangles_from_data(primitive_data)
            vg_name = str(i)
            vg_data = {
                "name": vg_name,
                "triangles": triangles,
                "material": materials[primitive_data['material_name']]
            }
            vertex_groups_data[vg_name] = vg_data
        mesh_data["vertex_groups"] = vertex_groups_data

        mesh = create_mesh(
            mesh_data=mesh_data,
            materials=materials,
            skeleton=skeleton,
            animations=animations,
            mode=mode,
            batch=batch,
            group=group,
            program=program,
            parent=scene_obj
        )
        scene_obj.children.append(mesh)
        scene.add_mesh(mesh)

    if node_data.get("children"):
        for child_data in node_data["children"]:
            child_obj = create_object(
                child_data,
                materials=materials,
                skeleton=skeleton,
                animations=animations,
                scene=scene,
                mode=mode,
                batch=batch,
                group=group,
                program=program,
                parent=scene_obj
            )
            scene_obj.children.append(child_obj)

    return scene_obj


def get_transform_from_node_data(node_data):
    transform = Transform()
    if node_data["translation"]:
        transform.translation = Vec3(*node_data["translation"])

    if node_data["rotation"]:
        q = Quaternion(node_data["rotation"][3], *node_data["rotation"][:3])
        rot_x, rot_y, rot_z = get_euler_angles(q)
        transform.rotation = Vec3(rot_x, rot_y, rot_z)

    if node_data["scale"]:
        transform.scale = Vec3(*node_data["scale"])
    return transform


def create_mesh(
    mesh_data: dict[str, Any],
    materials: dict[str, Material],
    skeleton: Skeleton | None,
    animations: dict[str, Animation],
    mode: GeometryMode = GeometryMode.TRIANGLES,
    batch: Batch | None = None,
    group: Group | None = None,
    program: ShaderProgram | None = None,
    transform: Transform = Transform(),
    parent: SceneObject | None = None
):
    # Create vertex groups
    vertex_groups: dict[str, VertexGroup] = {}
    for vg_name, vg_data in mesh_data['vertex_groups'].items():
        material = vg_data['material']
        vertex_groups[vg_name] = VertexGroup(
            vg_name, vg_data['triangles'], material
        )

    if skeleton and animations:
        mesh = SkeletalMesh(
            name=mesh_data["name"],
            vertex_groups=vertex_groups,
            materials=materials,
            skeleton=skeleton,
            animations=animations,
            mode=mode,
            batch=batch,
            group=group,
            program=program,
            transform=transform,
            parent=parent
        )
    else:
        mesh = Mesh(
            name=mesh_data["name"],
            vertex_groups=vertex_groups,
            materials=materials,
            mode=mode,
            batch=batch,
            group=group,
            program=program,
            transform=transform,
            parent=parent
        )
    return mesh


class GLTFLoader:
    @staticmethod
    def load(
        filename: str,
        scale: float = 1.0,
        mode: GeometryMode = GeometryMode.TRIANGLES,
        batch: Batch | None = None,
        group: Group | None = None,
        program: ShaderProgram | None = None
    ) -> tuple[list[Scene], list[Skeleton], dict[str, Animation]]:

        # We need a dict with data
        # parsed_data has a shape like this:
        # {
        #    "scenes_data": [
        #       {
        #           "name": Main,
        #           "nodes": [
        #               {
        #                   "name": "Armature",
        #                   "matrix": Mat4(),
        #                   "children": [
        #                       {
        #                           "name": "Ch10",
        #                           "mesh": {
        #                              "name": "Knight",
        #                              "primitives": [
        #                                  {
        #                                      "indices": [1, 2, 3, ...],
        #                                      "positions": [(132.4, 427.2,
        #                                      12.3), (...), ...],
        #                                      "material_name": "Wood"
        #                                  }
        #                              ]
        #                           }
        #                           "matrix": Mat4()
        #                       }
        #                   ]
        #               }
        #           ]
        #
        #    ],
        #     "materials_data": {
        #       "Wood": {
        #           "name": "Wood",
        #           "diffuse_color": (1.0, 1.0, 1.0, 1.0)
        #       },
        #       "Stone": {
        #           "name": "Stone",
        #           "diffuse_color": (0.98, 0.73, 0.56, 1.0)
        #       }
        #     }
        # }
        parsed_data = GLTFParser.parse(filename)
        scenes: list[Scene] = []
        skeletons: list[Skeleton] = []
        animations: dict[str, Animation] = {}

        # Create skins
        if parsed_data.get('skins_data'):
            for skeleton_data in parsed_data['skins_data']:
                skeleton = create_skeleton(skeleton_data)
                skeletons.append(skeleton)

        # Create animations
        if parsed_data.get('animations_data'):
            animations.update(load_animations(parsed_data['animations_data']))

        # Create materials
        materials = {}
        idx = 1
        for name, material_data in parsed_data["materials_data"].items():
            material = create_material(material_data, idx)
            materials[name] = material
            idx += 1

        # Create scenes
        skeleton = skeletons[0] if skeletons else None
        for scene_data in parsed_data["scenes_data"]:
            scene = Scene(scene_data["name"])
            for node_data in scene_data["nodes"]:
                scene_obj = create_object(
                    node_data,
                    materials=materials,
                    skeleton=skeleton,
                    animations=animations,
                    scene=scene,
                    mode=mode,
                    batch=batch,
                    group=group,
                    program=program
                )
                scene.objects.append(scene_obj)
            scenes.append(scene)

        return (scenes, skeletons, animations)
