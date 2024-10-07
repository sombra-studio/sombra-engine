import os
from pyglet.math import Vec2, Vec3


from sombra_engine.models.obj.mtl_loader import MTLLoader
from sombra_engine.primitives import Material, Triangle, Vertex


class OBJParser:
    """
    Class for parsing an OBJ file and storing the data in dictionaries.

    This class implements the parse method that reads an OBJ file and stores the
    information into dictionaries that are useful for another OBJLoader class.
    The OBJLoader class is the one responsible for creating a 3D model from an
    OBJ file, on the other hand this class (OBJParser) only deals with
    transforming the text into dictionaries, and loading the materials.

    Attributes:
        meshes_data: This dictionary has the name of a mesh as key and then
            another dictionary representing the data of that mesh as value.
        current_mesh_name: This string stores the name of the mesh that is
            currently being read in the OBJ file.
        current_vertex_group_name: This string stores the name of the vertex
            group that is currently being read in the OBJ file.
        materials: This dictionary has the name of a Material as key and that
            Material object as value.
    """

    def __init__(self):
        self.meshes_data: dict = {}
        self.current_mesh_name: str = "unnamed mesh"
        self.current_vertex_group_name: str = "unnamed vertex group"
        self.materials: dict[str, Material] = {}

    def parse(self, filename: str, scale: float = 1.0):
        """
        Parse a given OBJ file reading line by line and stores the model
        information into data structures that are attributes of this class.

        Args:
            filename: Path of an OBJ file
        """
        file = open(filename)
        path = os.path.dirname(filename)
        for line in file:
            if not line or line[0] == '#':
                continue
            # Remove end of line character
            if len(line) > 1 and line[-1] == '\n':
                line = line[:-1]
            args = line.split(' ')
            # Remove empty strings
            args = list(filter(lambda c: c != '', args))

            if args[0] == 'o':
                self.set_name(args[1])
            elif args[0] == 'v':
                self.set_vertex(args[1:], scale=scale)
            elif args[0] == 'vt':
                self.set_tex_coords(args[1:])
            elif args[0] == 'vn':
                self.set_normal(args[1:])
            elif args[0] == 'f':
                self.set_face(args[1:])
            elif args[0] == 'g':
                self.set_vertex_group(args[1])
            elif args[0] == 'mtllib':
                self.load_materials(os.path.join(path, args[1]))
            elif args[0] == 'usemtl':
                self.set_material(args[1])
        file.close()

    def get_current_mesh_data(self):
        if self.current_mesh_name not in self.meshes_data:
            # In this case the OBJ file doesn't define an 'o <modelName>'
            self.set_name(self.current_mesh_name)
        return self.meshes_data[self.current_mesh_name]

    def get_current_vertex_group(self):
        data = self.get_current_mesh_data()
        if self.current_vertex_group_name not in data['vertex_groups']:
            self.set_vertex_group(self.current_vertex_group_name)
        return data['vertex_groups'][self.current_vertex_group_name]

    def set_name(self, name: str):
        self.meshes_data[name] = {
            'name': name,
            'indices': [],
            'positions': [],
            'tex_coords': [],
            'normals': [],
            'vertex_groups': {}
        }
        self.current_mesh_name = name

    def set_vertex(self, args: list[str], scale: float = 1.0):
        data = self.get_current_mesh_data()
        positions = [float(x) for x in args]
        new_position = Vec3(*positions) * scale
        data['positions'].append(new_position)

    def set_face(self, args: list[str]):
        """
        Set a new face by reading the given arguments and stores it in the
        current mesh data dictionary. Will assume each element will always have
        two '/'.

        Args:
            args: the arguments of the set face command as a list,
                for ex. ['6/5/1', '7/3/2', '8/6/3']
                and this format f v1[/vt1][/vn1] v2[/vt2][/vn2] v3[/vt3][/vn3]
        """
        data = self.get_current_mesh_data()
        positions = data['positions']
        normals = data['normals']
        tex_coords = data['tex_coords']
        vg_data = self.get_current_vertex_group()
        new_vertices = []

        for vertex_str in args:
            # Split by '/' and transform the values to int
            indices_str = vertex_str.split('/')

            position_idx = int(indices_str[0]) - 1
            position = positions[position_idx]
            vertex = Vertex(position)
            if indices_str[1]:
                tex_coords_idx = int(indices_str[1]) - 1
                vertex.tex_coords = tex_coords[tex_coords_idx]
            if indices_str[2]:
                normal_idx = int(indices_str[2]) - 1
                vertex.normal = normals[normal_idx]
            new_vertices.append(vertex)
        new_triangle = Triangle(new_vertices)
        vg_data['triangles'].append(new_triangle)

    def set_tex_coords(self, args: list[str]):
        data = self.get_current_mesh_data()
        values = [float(x) for x in args]
        new_tex_coords = Vec2(*values[0:2])
        data['tex_coords'].append(new_tex_coords)

    def set_normal(self, args: list[str]):
        data = self.get_current_mesh_data()
        values = [float(x) for x in args]
        new_normal = Vec3(*values)
        data['normals'].append(new_normal)

    def set_vertex_group(self, name: str):
        data = self.get_current_mesh_data()
        self.current_vertex_group_name = name
        if name not in data['vertex_groups']:
            new_vg_data = {
                'name': name,
                'triangles': []
            }
            data['vertex_groups'][name] = new_vg_data

    def set_material(self, name: str):
        vg_data = self.get_current_vertex_group()
        if vg_data:
            if 'material' in vg_data:
                # In case of a vertex group that already has a material, create
                # a new vertex group
                self.current_vertex_group_name += "+"
                self.set_vertex_group(self.current_vertex_group_name)
                vg_data = self.get_current_vertex_group()
            vg_data['material'] = self.materials[name]

    def load_materials(self, filename: str):
        self.materials = MTLLoader.load(filename)
