from dataclasses import dataclass
from pyglet.math import Vec3
from pyglet.image import Texture


@dataclass
class Material:
    material_id: int
    name: str = "default"
    ambient: Vec3 = Vec3(1.0, 1.0, 1.0)
    diffuse: Vec3 = Vec3(1.0, 1.0, 1.0)
    specular: Vec3 = Vec3(0.0, 0.0, 0.0)
    specular_exponent: float = 0.0
    ior: float = 1.0
    bump_scale: float = 0.9
    ambient_map: Texture | None = None
    diffuse_map: Texture | None = None
    specular_map: Texture | None = None
    bump_map: Texture | None = None
    normal_map: Texture | None = None
    has_bump_map: bool = False
    has_normal_map: bool = False
    has_specular_map: bool = False

    def __hash__(self):
        return hash(self.material_id)

