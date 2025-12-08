from pyglet.gl import GL_TRIANGLES
from pyglet.graphics import Batch, Group, ShaderProgram
from pyglet.math import Mat4, Vec3

from sombra_engine.models import Bone, Model, SkeletalMesh
from sombra_engine.primitives import (
    Material, SceneObject, Transform,
    Triangle, Vertex, VertexGroup
)
from sombra_engine.models.gltf import GLTFParser


def get_triangles_from_data(data: dict) -> list[Triangle]:
    triangles = []
    num_vertices = len(data["indices"])
    for num_tri in range(num_vertices // 3):
        new_vertices = []
        for i in range(3):
            index = num_tri * 3 + i
            position: Vec3 = Vec3(*data["position"][index])
            vertex = Vertex(
                position=position,
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
            triangles = get_triangles_from_data(data)
            mesh_data = {
                "name": data["name"],
                "triangles": triangles,
                "material": materials_list[data["material"]],
            }
            meshes_data[name] = mesh_data

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
