from typing import TextIO

from pyglet.math import Vec2, Vec3
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram

from sombra_engine.constants import *
from sombra_engine.models import Mesh, Model
from sombra_engine.primitives import Material, Vertex, VertexGroup


class MtlParser:
    def __init__(self):
        self.current_name = None
        self.materials = {}
        self.commands_map = {
            'newmtl': self.set_new_material,
            'Ka': self.set_ambient,
            'Kd': self.set_diffuse,
            'Ks': self.set_specular,
            'Ns': self.set_specular_exponent,
            'Ni': self.set_ior,
        }

    def parse(self, file: TextIO):
        """
        Read a MTL file line by line parsing the commands and storing the
        information into data structures that are attributes of this class
        Args:
            file: A MTL file
        """
        for line in file:
            if not line or line[0] == '#':
                continue
            args = line.split(' ')
            command = args[0]
            if command in self.commands_map:
                self.commands_map[command](*args[1:])

    def set_new_material(self, name: str):
        self.current_name = name
        self.materials[name] = {}

    def set_color_by_key(self, key: str, r: str, g: str, b: str):
        if self.current_name is None:
            self.current_name = DEFAULT_MATERIAL_NAME
        self.materials[self.current_name][key] = Vec3(
            float(r), float(g), float(b)
        )

    def set_value_by_key(self, key: str, value: str):
        if self.current_name is None:
            self.current_name = DEFAULT_MATERIAL_NAME
        self.materials[self.current_name][key] = float(value)

    def set_ambient(self, r: str, g: str, b: str):
        self.set_color_by_key('ambient', r, g, b)

    def set_diffuse(self, r: str, g: str, b: str):
        self.set_color_by_key('diffuse', r, g, b)

    def set_specular(self, r: str, g: str, b: str):
        self.set_color_by_key('specular', r, g, b)

    def set_specular_exponent(self, value: str):
        self.set_value_by_key('specular_exponent', value)

    def set_ior(self, value: str):
        self.set_value_by_key('ior', value)


class MtlLoader:
    @staticmethod
    def load(filename: str) -> dict[str, Material]:
        mtl_parser = MtlParser()
        with open(filename) as f:
            mtl_parser.parse(f)
        return mtl_parser.materials


class OBJParser:
    def __init__(self):
        self.meshes_data = []
        self.vertex_groups_data = []
        self.current_mesh_data = {}
        self.current_vertex_group = {}
        self.materials = {}
        self.mtl_loader = MtlLoader()

    def parse(self, file: TextIO):
        """
        Parse a given OBJ file reading line by line and stores the model
        information into data structures that are attributes of this class.
        Args:
            file: An OBJ file
        """
        for line in file:
            if not line or line[0] == '#':
                continue
            args = line.split(' ')
            if args[0] == 'o':
                self.set_name(args[1])
            elif args[0] == 'v':
                self.set_vertex(args[1:])
            elif args[0] == 'vt':
                self.set_tex_coords(args[1:])
            elif args[0] == 'vn':
                self.set_normal(args[1:])
            elif args[0] == 'f':
                self.set_face(args[1:])
            elif args[0] == 's' or args[0] == 'g':
                self.set_vertex_group(args[1])
            elif args[0] == 'mtllib':
                self.load_materials(args[1])
            elif args[0] == 'usemtl':
                self.set_material(args[1])

        # Finally add the current pending data
        vg_data = self.current_vertex_group
        if vg_data:
            if 'vertex_groups' in self.current_mesh_data:
                new_vertex_group = VertexGroup(
                    vg_data['name'], vg_data['indices'], vg_data['material']
                )
                self.current_mesh_data['vertex_groups'].append(new_vertex_group)
        mesh_data = self.current_mesh_data
        if mesh_data:
            self.meshes_data.append(mesh_data)

    def set_name(self, name: str):
        # If we already have a current mesh data we append it
        if self.current_mesh_data:
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
        vg_data = self.current_vertex_group

        for indices_str in args:
            # Split by '/' and transform the values to int
            values_str = indices_str.split('/')

            idx = int(values_str[0]) - 1
            self.current_mesh_data['indices'].append(idx)
            if vg_data:
                self.current_vertex_group['indices'].append(idx)
            vertex = vertices[idx]
            if values_str[1]:
                tex_coords_idx = int(values_str[1]) - 1
                vertex.tex_coords = tex_coords[tex_coords_idx]
            if values_str[2]:
                normal_idx = int(values_str[2]) - 1
                vertex.normal = normals[normal_idx]

    def set_tex_coords(self, args: list[str]):
        if 'tex_coords' not in self.current_mesh_data:
            self.current_mesh_data['tex_coords'] = []

        values = [float(x) for x in args]
        new_tex_coords = Vec2(values[0], values[1])
        self.current_mesh_data['tex_coords'].append(new_tex_coords)

    def set_normal(self, args: list[str]):
        if 'normals' not in self.current_mesh_data:
            self.current_mesh_data['normals'] = []

        values = [float(x) for x in args]
        new_normal = Vec2(values[0], values[1])
        self.current_mesh_data['normals'].append(new_normal)

    def set_vertex_group(self, name: str):
        vg_data = self.current_vertex_group
        if vg_data:
            if 'vertex_groups' in self.current_mesh_data:
                new_vertex_group = VertexGroup(
                    vg_data['name'], vg_data['indices'], vg_data['material']
                )
                self.current_mesh_data['vertex_groups'].append(new_vertex_group)
        vg_data['name'] = name

    def set_material(self, name: str):
        vg_data = self.current_vertex_group
        if vg_data:
            vg_data['material'] = self.materials[name]
            
    def load_materials(self, filename: str):
        self.materials = self.mtl_loader.load(filename)


class OBJLoader:
    @staticmethod
    def load(
        filename: str, name: str, program: ShaderProgram, batch: Batch = None,
        group: Group = None
    ) -> Model:
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
