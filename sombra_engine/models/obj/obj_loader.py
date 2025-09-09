from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram


from sombra_engine.models import Mesh, Model, SkeletalMesh
from .obj_parser import OBJParser
from sombra_engine.primitives import VertexGroup


class OBJLoader:
    @staticmethod
    def load(
        filename: str,
        name: str = "unnamed object",
        program: ShaderProgram = None,
        scale: float = 1.0,
        batch: Batch = None,
        group: Group = None
    ) -> Model:
        obj_parser = OBJParser()
        # Parse the file
        obj_parser.parse(filename, scale=scale)

        # Now create the Model
        meshes = []
        for mesh_data in obj_parser.meshes_data.values():
            # Create Vertex Groups
            vertex_groups: dict[str, VertexGroup] = {}
            for vg_data in mesh_data['vertex_groups'].values():
                vertex_groups[vg_data['name']] = VertexGroup(
                    vg_data['name'], vg_data['triangles'], vg_data['material']
                )
            # Create Mesh
            new_mesh = Mesh(
            # new_mesh = SkeletalMesh(
                mesh_data['name'],
                vertex_groups=vertex_groups,
                materials=obj_parser.materials,
                batch=batch,
                group=group,
                program=program
            )
            meshes.append(new_mesh)
        model = Model(name, meshes)
        return model
