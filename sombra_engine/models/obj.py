from pyglet.math import Vec3
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram


from sombra_engine.models import Mesh, Model
from sombra_engine.primitives import Vertex


def set_triangle(args, params):
    values = args[1].split('/')
    if len(values) == 1:
        params['indices'] += args[1:]
    elif len(values) == 2:
        if '//' in args[1]:
            vertices = params['vertices']
            normals = params['normals']
            for data in args[1:]:
                values = data.split('/')
                vert_id = int(values[0])
                vertex = vertices[vert_id - 1]
                params['indices'].append(vert_id)
                normal_idx = int(values[2]) - 1
                vertex.normal = normals[normal_idx]
        else:
            vertices = params['vertices']
            tex_coords = params['tex_coords']
            for data in args[1:]:
                values = data.split('/')
                vert_id = int(values[0])
                vertex = vertices[vert_id - 1]
                params['indices'].append(vert_id)
                tex_coords_idx = int(values[1]) - 1
                vertex.tex_coords = tex_coords[tex_coords_idx]
    else:
        vertices = params['vertices']
        normals = params['normals']
        tex_coords = params['tex_coords']
        for data in args[1:]:
            values = data.split('/')
            vert_id = int(values[0])
            vertex = vertices[vert_id - 1]
            params['indices'].append(vert_id)
            tex_coords_idx = int(values[1]) - 1
            vertex.tex_coords = tex_coords[tex_coords_idx]
            normal_idx = int(values[2]) - 1
            vertex.normal = normals[normal_idx]


class OBJLoader:
    @staticmethod
    def load(
        filename: str, name: str, program: ShaderProgram, batch: Batch = None,
        group: Group = None
    ):
        meshes = []
        current_mesh_params = {}
        # Parse the file
        with open(filename) as f:
            for line in f:
                if not line or line[0] == '#':
                    continue
                args = line.split(' ')
                if args[0] == 'o':
                    # set name
                    if current_mesh_params.keys():
                        meshes.append(current_mesh_params)
                    current_mesh_params = {}
                    current_mesh_params['name'] = args[1]
                elif args[0] == 'v':
                    # set vertex
                    if not 'vertices' in current_mesh_params:
                        current_mesh_params['vertices'] = []
                    else:
                        new_vert = Vertex(
                            len(current_mesh_params['vertices']) + 1,
                            position=Vec3(*args[1:])
                        )
                        current_mesh_params['vertices'].append(new_vert)
                elif args[0] == 'f':
                    # set triangle
                    set_triangle(args, current_mesh_params)


        # Now create the Model
        for i, m in enumerate(meshes):
            # Create Mesh
            meshes[i] = Mesh(
                m['name'],
                m['vertices'],
                m['indices'],
                vertex_groups=m['vertex_groups'],
                materials=m['materials'],
                batch=batch,
                group=group,
                program=program
            )
        model = Model(name, meshes)
        return model
