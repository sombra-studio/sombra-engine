from typing import TextIO

from pyglet.math import Vec3
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram


from sombra_engine.models import Mesh, Model
from sombra_engine.primitives import Vertex


class OBJParser:
    def __init__(self):
        self.meshes_data = []
        self.current_mesh_data = {}

    def set_name(self, name: str):
        # If we already have a current mesh data we append it
        if self.current_mesh_data.keys():
            self.meshes_data.append(self.current_mesh_data)
        self.current_mesh_data = {'name': name}

    def set_vertex(self, args: list[str]):
        if 'vertices' not in self.current_mesh_data:
            self.current_mesh_data['vertices'] = []

        positions = map(float, args)
        new_vert = Vertex(
            len(self.current_mesh_data['vertices']) + 1,
            position=Vec3(*positions)
        )
        self.current_mesh_data['vertices'].append(new_vert)

    def set_face(self, args: list[str]):
        """
        Set a new face by reading the given arguments and stores it in the
        current mesh data dictionary. Will assume each element will always have
        two '/'.

        Args:
            args: the arguments of the set face command as a list,
                for ex. ['6/5/1', '7/3/2', '8/6/3']
        """
        vertices = self.current_mesh_data['vertices']
        normals = self.current_mesh_data['normals']
        tex_coords = self.current_mesh_data['tex_coords']

        for indices_str in args:
            # Split by '/' and transform the values to int
            values_str = indices_str.split('/')

            idx = int(values_str[0]) - 1
            self.current_mesh_data['indices'].append(idx)
            vertex = vertices[idx]
            if values_str[1]:
                tex_coords_idx = int(values_str[1]) - 1
                vertex.tex_coords = tex_coords[tex_coords_idx]
            if values_str[2]:
                normal_idx = int(values_str[2]) - 1
                vertex.normal = normals[normal_idx]

    def parse(self, file: TextIO):
        for line in file:
            if not line or line[0] == '#':
                continue
            args = line.split(' ')
            if args[0] == 'o':
                self.set_name(args[1])
            elif args[0] == 'v':
                self.set_vertex(args[1:])
            elif args[0] == 'f':
                self.set_face(args[1:])


class OBJLoader:
    @staticmethod
    def load(
        filename: str, name: str, program: ShaderProgram, batch: Batch = None,
        group: Group = None
    ):
        obj_parser = OBJParser()
        # Parse the file
        with open(filename) as f:
            obj_parser.parse(f)

        # Now create the Model
        meshes = []
        for mesh_data in obj_parser.meshes_data:
            # Create Mesh
            new_mesh = Mesh(
                mesh_data['name'],
                mesh_data['vertices'],
                mesh_data['indices'],
                vertex_groups=mesh_data['vertex_groups'],
                materials=mesh_data['materials'],
                batch=batch,
                group=group,
                program=program
            )
            meshes.append(new_mesh)
        model = Model(name, meshes)
        return model
