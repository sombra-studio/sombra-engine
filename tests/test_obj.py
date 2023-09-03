from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Mat4, Vec2, Vec3
import unittest


from sombra_engine.models.obj import MTLLoader, OBJLoader
from sombra_engine.primitives import Material


class MTLTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = 'data/plane.mtl'
        self.materials = MTLLoader.load(self.filename)

    def test_mtl_loader(self):
        # Test first material
        name = 'Material.001'
        self.assertIn(name, self.materials)
        mtl = self.materials[name]
        mtl_copy = Material(
            material_id=1,
            name=name,
            diffuse=Vec3(0.279282, 0.015609, 0.800000),
            specular=Vec3(0.5, 0.5, 0.5),
            specular_exponent=250,
            ior=1.45
        )
        self.assertEqual(mtl, mtl_copy)
        mtl_copy.diffuse = Vec3(1.0, 0.5, 1.0)
        self.assertNotEqual(mtl, mtl_copy)

        # Test second material
        name = 'Material.002'
        self.assertIn(name, self.materials)
        mtl = self.materials[name]
        mtl_copy = Material(
            material_id=2,
            name=name,
            ambient=Vec3(0.100000, 0.100000, 0.100000),
            diffuse=Vec3(0.938000, 0.837642, 0.527156),
            specular=Vec3(0.500000, 0.500000, 0.500000),
            specular_exponent=39.999996,
            ior=1.5
        )
        self.assertEqual(self.materials[name], mtl_copy)
        self.assertEqual(mtl, mtl_copy)
        mtl_copy.diffuse = Vec3(1.0, 0.5, 1.0)
        self.assertNotEqual(mtl, mtl_copy)


class OBJTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = 'data/plane.obj'
        with open('data/test.vert') as f:
            self.vert_shader = Shader(f.read(), 'vertex')
        with open('data/test.frag') as f:
            self.frag_shader = Shader(f.read(), 'fragment')
        self.program = ShaderProgram(self.vert_shader, self.frag_shader)
        self.program['mv'] = Mat4()
        self.program['proj'] = Mat4()

    def test_model(self):
        name = 'test'
        vertices = [
            Vec3(-1, 0, 1), Vec3(1, 0, 1), Vec3(-1, 0, -1), Vec3(1, 0, -1)
        ]
        normal = Vec3(0, 1, 0)
        tex_coords = [Vec2(0, 0), Vec2(1, 0), Vec2(0, 1), Vec2(1, 1)]
        indices = [1, 2, 0, 1, 3, 2]

        model = OBJLoader.load(self.filename, 'test', self.program)
        self.assertEqual(model.name, name)
        plane = model.meshes[0]
        self.assertEqual(plane.name, 'Plane')
        for i, vertex in enumerate(plane.vertices):
            self.assertEqual(vertex.position, vertices[i])
            self.assertEqual(vertex.normal, normal)

        self.assertEqual(plane.indices, indices)

        for idx in indices:
            self.assertEqual(
                plane.vertices[idx - 1].tex_coords, tex_coords[idx - 1]
            )


if __name__ == '__main__':
    unittest.main()
