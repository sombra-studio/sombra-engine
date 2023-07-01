from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Mat4
import unittest


from sombra_engine.models.obj import MTLLoader, OBJLoader


class MTLTestCase(unittest.TestCase):
    def setUp(self):
        self.filename = 'data/plane.mtl'
        self.materials = MTLLoader.load(self.filename)

    def test_mtl_loader(self):
        name = 'Material.001'
        self.assertIn(name, self.materials)

"""
newmtl Material.001
Ns 250.000000
Ka 1.000000 1.000000 1.000000
Kd 0.279282 0.015609 0.800000
Ks 0.500000 0.500000 0.500000
Ke 0.000000 0.000000 0.000000
Ni 1.450000
d 1.000000
illum 2
"""


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
        vertices = [(-1, 0, 1), (1, 0, 1), (-1, 0, -1), (1, 0, -1)]
        normal = (0, 1, 0)
        tex_coords = [(0, 0), (1, 0), (0, 1), (1, 1)]
        indices = [1, 2, 0, 1, 3, 2]

        model = OBJLoader.load(self.filename, 'test', self.program)
        self.assertEqual(model.name, name)
        plane = model.meshes[0]
        self.assertEqual(plane.name, 'Plane')
        for i, vertex in enumerate(plane.vertices):
            self.assertEqual(vertex.get_attr_tuple('position'), vertices[i])

        self.assertEqual(plane.indices, indices)
        self.assertEqual(plane.vertices[0].normal, normal)

        for idx in indices:
            self.assertEqual(
                plane.vertices[idx - 1].tex_coords.x, tex_coords[idx - 1]
            )


if __name__ == '__main__':
    unittest.main()

"""
mtllib plane.mtl
o Plane
v -1.000000 0.000000 1.000000
v 1.000000 0.000000 1.000000
v -1.000000 0.000000 -1.000000
v 1.000000 0.000000 -1.000000
vn -0.0000 1.0000 -0.0000
vt 0.000000 0.000000
vt 1.000000 0.000000
vt 0.000000 1.000000
vt 1.000000 1.000000
s 0
usemtl Material.001
f 2/2/1 3/3/1 1/1/1
f 2/2/1 4/4/1 3/3/1
"""
