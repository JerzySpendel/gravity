import unittest
import bhtree
import planet
import constants


class BHNodeTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.t = bhtree.BHTree()
        self.planet_nw = planet.Planet(None, r=[0, 260])
        self.planet_ne = planet.Planet(None, r=[280, 260])
        self.planet_sw1 = planet.Planet(None, r=[0, 0])
        self.planet_sw2 = planet.Planet(None, r=[240, 0])
        self.planet_sw3 = planet.Planet(None, r=[120, 0])
        self.little_nodes = []
        for i in range(1, 10):
            node = bhtree.BHTree.BHNode(bhtree.Area(i, i, 1))
            self.little_nodes.append(node)

    def test_area_from_node(self):
        BHNode = bhtree.BHTree.BHNode
        area = BHNode.area_from_node(self.t.root, 'nw')
        self.assertEqual(area, bhtree.Area(0, 499, 250))
        area = BHNode.area_from_node(self.t.root, 'ne')
        self.assertEqual(area, bhtree.Area(250, 499, 250))
        area = BHNode.area_from_node(self.t.root, 'sw')
        self.assertEqual(area, bhtree.Area(0, 249, 250))
        area = BHNode.area_from_node(self.t.root, 'se')
        self.assertEqual(area, bhtree.Area(250, 249, 250))

    def test_which_part(self):
        BHNode = bhtree.BHTree.BHNode
        self.assertEqual(self.t.root.which_part(self.planet_nw), 'nw')
        self.assertEqual(self.t.root.which_part(self.planet_ne), 'ne')

    def test_adding_planet(self):
        self.t.add_planet(self.planet_sw1)
        self.t.add_planet(self.planet_sw2)
        self.t.add_planet(self.planet_sw3)
        self.assertIn(self.planet_sw1, self.t.root)
        self.assertIn(self.planet_sw2, self.t.root)
        self.assertIn(self.planet_sw3, self.t.root)

    def test_mass(self):
        self.t.add_planet(self.planet_sw1)
        self.t.add_planet(self.planet_sw2)
        self.assertEqual(self.t.root.mass, 2*constants.STANDARD_PLANET_MASS)
        self.t.add_planet(self.planet_sw3)
        self.assertEqual(self.t.root.mass, 3*constants.STANDARD_PLANET_MASS)

    def test_simple_mass_center(self):
        self.t.add_planet(self.planet_sw1)
        self.t.add_planet(self.planet_sw2)
        x = (self.planet_sw1.r[0] + self.planet_sw2.r[0])/2
        y = (self.planet_sw1.r[1] + self.planet_sw2.r[1])/2
        self.assertEqual(self.t.root.mass_center, (x, y))

    def test_little_areas_division(self):
        node = bhtree.BHTree.BHNode(bhtree.Area(0, 1, 1))
        self.assertEqual(node.area_from_node(node, 'sw'), bhtree.Area(0, 0.5, 0.5))
        self.assertEqual(node.area_from_node(node, 'se'), bhtree.Area(0.5, 0.5, 0.5))
        self.assertEqual(node.area_from_node(node, 'nw'), bhtree.Area(0, 1, 0.5))
        self.assertEqual(node.area_from_node(node, 'ne'), bhtree.Area(0.5, 1, 0.5))

    def test_little_may_contain(self):
        for i in range(1, 10):
            node = self.little_nodes[i-1]
            self.assertTrue(node.may_contain(planet.Planet(None, r=[i, i])))
