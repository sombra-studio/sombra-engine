from pyglet.gl import GL_TRIANGLES
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram
from pyglet.math import Mat4, Vec2, Vec3

from sombra_engine.models import Bone, Model, SkeletalMesh
from sombra_engine.primitives import (
    Material, SceneObject, Transform,
    Triangle, Vertex, VertexGroup
)
from sombra_engine.models.gltf import GLTFParser


def get_triangles_from_data(data: dict) -> list[Triangle]:
    triangles = []
    num_vertices = len(data["indices"])
    for tri_num in range(num_vertices // 3):
        new_vertices = []
        for i in range(3):
            index = data["indices"][tri_num * 3 + i]
            position: Vec3 = Vec3(*data["positions"][index])
            normal: Vec3 = Vec3(*data["normals"][index])
            tex_coords: Vec2 = Vec2(*data["tex_coords"][index])
            vertex = Vertex(
                position=position,
                normal=normal,
                tex_coords=tex_coords,
            )
            new_vertices.append(vertex)
        new_triangle = Triangle(new_vertices)
        triangles.append(new_triangle)
    return triangles



class GLTFLoader:
    @staticmethod
    def load(
        filename: str,
        name: str | None = None,
        scale: float = 1.0,
        mode: int = GL_TRIANGLES,
        batch: Batch = None,
        group: Group = None,
        program: ShaderProgram = None,
        transform: Transform = Transform(),
        parent: SceneObject = None
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
        #     "materials_data": [
        #       {
        #           "name": "Wood",
        #           "diffuse_color": (1.0, 1.0, 1.0, 1.0)
        #       }
        #     ]
        # }
        parsed_data = GLTFParser.parse(filename, scale=scale)
        meshes_data = {}

        # Create materials
        materials_list = []
        for idx, material_data in enumerate(parsed_data["materials_data"]):
            name = material_data["name"]
            material = Material(
                material_id=idx,
                name=name,
                diffuse=material_data["diffuse"],
            )
            materials_list.append(material)

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
                    "material": materials_list[primitive_data["material"]],
                }
                vertex_groups_data[vg_name] = vg_data
            meshes_data[name] = {
                'vertex_groups': vertex_groups_data
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

            # Create skeleton
            root = Bone(idx=1, name="root", local_bind_transform=Mat4())
                # iterate bones hierarchy

            # Create mesh
            mesh = SkeletalMesh(
                name=mesh_name,
                vertex_groups=vertex_groups,
                materials=materials,
                root_bone=root,
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
