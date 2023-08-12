from pyglet.gl import *
from pyglet.graphics import ShaderGroup, Group
from pyglet.image import Texture


from sombra_engine.primitives import Material


class MaterialGroup(ShaderGroup):
    def __init__(
        self, material: Material, program: pyglet.graphics.shader.ShaderProgram,
        order: int = 0, parent: Group = None
    ):
        super().__init__(program, order, parent)
        self.material = material


    def set_state(self):
        glEnable(GL_DEPTH_TEST)
        material = self.program.uniform_blocks['Material'].create_ubo()
        material.ambient = self.material.ambient
        material.diffuse = self.material.diffuse
        material.specular = self.material.specular
        material.specular_exponent = self.material.specular_exponent


class TexturedMaterialGroup(MaterialGroup):
    def set_state(self):
        glEnable(GL_DEPTH_TEST)
        material = self.program.uniform_blocks['TexturedMaterial'].create_ubo()
        ambient_map = self.get_ambient_map()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(ambient_map.target, ambient_map.id)
        diffuse_map = self.get_diffuse_map()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(diffuse_map.target, diffuse_map.id)
        specular_map = self.get_specular_map()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(specular_map.target, specular_map.id)
        material.specular_exponent = self.material.specular_exponent

    def get_ambient_map(self) -> Texture:
        if self.material.ambient_map:
            return self.material.ambient_map

    def get_diffuse_map(self) -> Texture:
        pass

    def get_specular_map(self) -> Texture:
        pass

