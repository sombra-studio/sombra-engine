from pyglet.math import Vec3


class Material:
    def __init__(
        self,
        material_id: int,
        name: str = "default",
        ambient: Vec3 = Vec3(1.0, 1.0, 1.0),
        diffuse: Vec3 = Vec3(1.0, 1.0, 1.0),
        specular: Vec3 = Vec3(1.0, 1.0, 1.0),
        specular_exponent: float = 0.0,
        ior: float = 1.0,
        bump_scale: float = 0.9,
        ambient_map: str = "",
        diffuse_map: str = "",
        specular_map: str = "",
        bump_map: str = ""
    ):
        self.material_id = material_id
        self.name = name
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.specular_exponent = specular_exponent
        self.ior = ior
        self.bump_scale = bump_scale
        self.ambient_map = ambient_map
        self.diffuse_map = diffuse_map
        self.specular_map = specular_map
        self.bump_map = bump_map
        self.has_bump_map = bump_map != ""
        self.has_specular_map = specular_map != ""

    def __hash__(self):
        return hash((self.material_id, self.name))

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Material) and
            self.material_id == other.material_id and
            self.name == other.name and
            self.ambient == other.ambient and
            self.diffuse == other.diffuse and
            self.specular == other.specular and
            self.specular_exponent == other.specular_exponent and
            self.ior == other.ior and
            self.ambient_map == other.ambient_map and
            self.diffuse_map == other.diffuse_map and
            self.specular_map == other.specular_map and
            self.bump_map == other.bump_map
        )
