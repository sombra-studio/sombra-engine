from pyglet.graphics import Batch, Group, ShaderProgram
import pyglet
from pyglet.math import Mat4

from sombra_engine.models import Bone, Model, SkeletalMesh
from sombra_engine.primitives import Material, SceneObject, VertexGroup


class GLTFLoader:
    @staticmethod
    def load(
        filename: str,
        name: str | None = None,
        program: ShaderProgram | None = None,
        scale: float = 1.0,
        batch: Batch | None = None,
        group: Group | None = None,
        parent: SceneObject | None = None
    ) -> Model:

        # Decode glTF file
        decoder = pyglet.model.ModelDecoder()
        gltf = decoder.decode(filename)

        # We need a dict with data
        meshes_data = gltf.meshes_data

        if name is None:
            name = filename

        meshes = []

        for mesh_name, mesh_data in meshes_data.items():
            # Create vertex groups
            vertex_groups: dict[str, VertexGroup] = {}
            for vg_name, vg_data in mesh_data['vertex_groups'].values():
                vertex_groups[vg_name] = VertexGroup(
                    vg_name, vg_data['triangles'], vg_data['material']
                )

            # Create skeleton
            root = Bone(idx=1, name="root", local_bind_transform=Mat4())
            # iterate bones

            # Create materials
            materials = {}
            for material_name, material_data in mesh_data['materials'].items():
                materials[material_name] = Material(
                    material_id=material_data,
                    name=material_name,
                    ambient=material_data['ambient'],
                )

            # Create mesh
            mesh = SkeletalMesh(
                name=mesh_name,
                vertex_groups=vertex_groups,
                materials=materials,
                root_bone=root,
                batch=batch,
                group=group,
                parent=parent
            )
            meshes.append(mesh)

        model = Model(
            name=name,
            meshes=meshes,
            parent=parent
        )
        return model
