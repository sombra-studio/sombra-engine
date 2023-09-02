from .mtl_parser import MTLParser
from sombra_engine.primitives import Material


class MTLLoader:
    @staticmethod
    def load(filename: str) -> dict[str, Material]:
        materials = {}
        mtl_parser = MTLParser()
        mtl_parser.parse(filename)
        material_id = 1
        for name, data in mtl_parser.materials.items():
            materials[name] = Material(material_id=material_id, **data)
            material_id += 1
        return materials
