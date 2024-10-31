import os
from pyglet.math import Vec3


from sombra_engine.constants import DEFAULT_MATERIAL_NAME


class MTLParser:
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
            'map_Ka': self.set_ambient_map,
            'map_Kd': self.set_diffuse_map,
            'map_Ks': self.set_specular_map,
            'map_bump': self.set_bump_map,
            'map_Bump': self.set_bump_map,
            'bump': self.set_bump_map
        }
        self.current_path = None

    def parse(self, filename: str):
        """
        Read an MTL file line by line parsing the commands and storing the
        information into data structures that are attributes of this class
        Args:
            filename: Path of an MTL file
        """
        self.current_path = os.path.dirname(filename)
        with open(filename) as file:
            for line in file:
                if not line or line[0] == '#':
                    continue
                # Remove end of line character
                if len(line) > 1 and line[-1] == '\n':
                    line = line[:-1]
                args = line.split(' ')
                # Remove empty strings
                args = [
                    arg.replace('\t', '')
                    for arg in args if arg != ''
                ]

                command = args[0]
                if command in self.commands_map:
                    self.commands_map[command](*args[1:])

    def set_new_material(self, name: str):
        self.current_name = name
        self.materials[name] = {'name': name}

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

    def set_map_by_key(self, key: str, filename: str):
        if self.current_name is None:
            self.current_name = DEFAULT_MATERIAL_NAME
        path = f"{self.current_path}/{filename}"
        self.materials[self.current_name][key] = path

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

    def set_ambient_map(self, filename: str):
        self.set_map_by_key('ambient_map', filename)

    def set_diffuse_map(self, filename: str):
        self.set_map_by_key('diffuse_map', filename)

    def set_specular_map(self, filename: str):
        self.set_map_by_key('specular_map', filename)

    def set_bump_map(self, filename: str):
        self.set_map_by_key('bump_map', filename)
