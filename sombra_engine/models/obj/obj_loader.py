from pyglet.graphics import Batch, Group, ShaderProgram


from sombra_engine.models import Mesh
from .obj_parser import OBJParser
from sombra_engine.primitives import VertexGroup
from sombra_engine import Scene


class OBJLoader:
    @staticmethod
    def load(
        filename: str,
        name: str = "unnamed object",
        program: ShaderProgram | None = None,
        scale: float = 1.0,
        batch: Batch | None = None,
        group: Group | None = None
    ) -> Scene:
        obj_parser = OBJParser()
        # Parse the file
        obj_parser.parse(filename, scale=scale)

        # Now create the scene
        scene = Scene()
        for mesh_data in obj_parser.meshes_data.values():
            # Create Vertex Groups
            vertex_groups: dict[str, VertexGroup] = {}
            for vg_data in mesh_data['vertex_groups'].values():
                vertex_groups[vg_data['name']] = VertexGroup(
                    vg_data['name'], vg_data['triangles'], vg_data['material']
                )
            # Create Mesh
            new_mesh = Mesh(
                mesh_data['name'],
                vertex_groups=vertex_groups,
                materials=obj_parser.materials,
                batch=batch,
                group=group,
                program=program
            )
            scene.add_mesh(new_mesh)

        return scene
