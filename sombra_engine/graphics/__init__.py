from pyglet.gl import *
from pyglet.graphics import ShaderGroup, Group


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
        ambient_map = self.material.ambient_map
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(ambient_map.target, ambient_map.id)
        diffuse_map = self.material.diffuse_map
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(diffuse_map.target, diffuse_map.id)
        specular_map = self.material.specular_map
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(specular_map.target, specular_map.id)
