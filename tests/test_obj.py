from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Mat4, Vec3
import unittest


from sombra_engine.models.obj import MTLLoader, OBJLoader


class MTLTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = 'tests/data/plane.mtl'
        self.materials = MTLLoader.load(self.filename)

    def test_mtl_loader(self):
        # Test first material
        name = 'Material.001'
        self.assertIn(name, self.materials)
        mtl = self.materials[name]
        self.assertEqual(mtl.material_id, 1)
        self.assertEqual(mtl.name, name)
        self.assertEqual(mtl.diffuse, Vec3(0.279282, 0.015609, 0.800000))
        self.assertEqual(mtl.specular, Vec3(0.5, 0.5, 0.5))
        self.assertEqual(mtl.specular_exponent, 250)
        self.assertEqual(mtl.ior, 1.45)

        # Test second material
        name = 'Material.002'
        self.assertIn(name, self.materials)
        mtl = self.materials[name]
        self.assertEqual(mtl.material_id, 2)
        self.assertEqual(mtl.name, name)
        self.assertEqual(mtl.ambient, Vec3(0.1, 0.1, 0.1))
        self.assertEqual(mtl.diffuse, Vec3(0.938000, 0.837642, 0.527156))
        self.assertEqual(mtl.specular, Vec3(0.5, 0.5, 0.5))
        self.assertEqual(mtl.specular_exponent, 39.999996)
        self.assertEqual(mtl.ior, 1.5)


class OBJTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = 'tests/data/plane.obj'
        with open('tests/data/test.vert') as f:
            self.vert_shader = Shader(f.read(), 'vertex')
        with open('tests/data/test.frag') as f:
            self.frag_shader = Shader(f.read(), 'fragment')
        self.program = ShaderProgram(self.vert_shader, self.frag_shader)
        self.program['mv'] = Mat4()
        self.program['proj'] = Mat4()

    def test_model(self):
        name = 'test'
        vertices = [
            1.0, 0.0, 1.0, -1.0, 0.0, -1.0, -1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
            1.0, 0.0, -1.0, -1.0, 0.0, -1.0
        ]
        normal = [
            -0.0, 1.0, -0.0, -0.0, 1.0, -0.0, -0.0, 1.0, -0.0, -0.0, 1.0, -0.0,
            -0.0, 1.0, -0.0, -0.0, 1.0, -0.0
        ]
        tangent = [
            1.0, 0.0, -0.0, 1.0, 0.0, -0.0, 1.0, 0.0, -0.0, 1.0, 0.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 0.0, 0.0
        ]
        tex_coords = [
            1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0
        ]

        model = OBJLoader.load(
            self.filename, 'test', program=self.program
        )
        self.assertEqual(model.name, name)
        plane_mesh = model.meshes[0]
        position_list, normal_list, tangent_list, tex_coords_list  = (
            plane_mesh.get_lists_for_vertex_group('unnamed vertex group')
        )
        self.assertEqual(position_list, vertices)
        self.assertEqual(normal_list, normal)
        self.assertEqual(tangent_list, tangent)
        self.assertEqual(tex_coords_list, tex_coords)


if __name__ == '__main__':
    unittest.main()
