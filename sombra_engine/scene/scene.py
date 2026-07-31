from pyglet.graphics import ShaderProgram
from pyglet.math import Vec3


from sombra_engine.models import Mesh, SkeletalMesh
from sombra_engine.primitives import SceneObject
from sombra_engine.scene import Light


class Scene:
    def __init__(self, name: str = "undefined"):
        self.name = name
        self.lights: list[Light] = []
        self.meshes: list[Mesh | SkeletalMesh] = []
        self.objects: list[SceneObject] = []

    def create_light(self, position: Vec3, color: Vec3):
        light = Light(position, color)
        self.lights.append(light)

        for mesh in self.meshes:
            # Update the light in every mesh
            program: ShaderProgram = mesh.program
            if 'light.position' in program.uniforms:
                program['light.position'] = self.lights[0].position
            if 'light.color' in program.uniforms:
                program['light.color'] = self.lights[0].color

    def remove_light(self, idx: int):
        self.lights.pop(idx)

    def add_mesh(self, mesh: Mesh | SkeletalMesh):
        program: ShaderProgram = mesh.program
        if 'light.position' in program.uniforms:
            if self.lights:
                program['light.position'] = self.lights[0].position
        if 'light.color' in program.uniforms:
            if self.lights:
                program['light.color'] = self.lights[0].color

        self.meshes.append(mesh)
