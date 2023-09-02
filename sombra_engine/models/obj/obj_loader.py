from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram


from sombra_engine.models import Mesh, Model
from .obj_parser import OBJParser
from sombra_engine.primitives import VertexGroup


class OBJLoader:
    @staticmethod
    def load(
        filename: str, name: str, program: ShaderProgram = None,
        batch: Batch = None, group: Group = None
    ) -> Model:
        obj_parser = OBJParser()
        # Parse the file
        obj_parser.parse(filename)

        # Now create the Model
        meshes = []
        for mesh_data in obj_parser.meshes_data.values():
            # Create Vertex Groups
            vertex_groups: dict[str, VertexGroup] = {}
            for vg_data in mesh_data['vertex_groups'].values():
                vertex_groups[vg_data['name']] = VertexGroup(
                    vg_data['name'], vg_data['indices'], vg_data['material']
                )
            # Create Mesh
            new_mesh = Mesh(
                mesh_data['name'],
                mesh_data['vertices'],
                mesh_data['indices'],
                vertex_groups=vertex_groups,
                materials=obj_parser.materials,
                batch=batch,
                group=group,
                program=program
            )
            meshes.append(new_mesh)
        model = Model(name, meshes)
        return model
