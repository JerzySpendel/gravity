from collections import namedtuple
from constants import PHI
import planet
import math

Area = namedtuple('Area', ['x', 'y', 'width'])


class BHTree:
    phi = PHI

    class BHNode:
        def __init__(self, area, nw=None, ne=None, sw=None, se=None):
            self.nw = nw
            self.ne = ne
            self.sw = sw
            self.se = se
            self.area = area

        @property
        def mass_center(self):
            node_mass = self.mass
            x, y = 0, 0
            for element in self:
                if isinstance(element, planet.Planet):
                    x += element.r[0]*element.mass/node_mass
                    y += element.r[1]*element.mass/node_mass
            return x, y

        @property
        def mass(self):
            mass = 0
            for quarter in 'nw', 'ne', 'sw', 'se':
                xx = getattr(self, quarter)
                if isinstance(xx, planet.Planet):
                    mass += xx.mass
                elif isinstance(xx, BHTree.BHNode):
                    mass += xx.mass
            return mass

        def mass_center_distance(self, _planet):
            mass_center = self.mass_center
            to_sqrt = (_planet.r[0]-mass_center[0])**2 + (_planet.r[1]-mass_center[1])**2
            return math.sqrt(to_sqrt)

        def add_planet(self, _planet):
            if _planet in self:
                return
            part = self.which_part(_planet)
            if isinstance(getattr(self, part), planet.Planet):
                removed_planet = getattr(self, part)
                setattr(self, part, BHTree.BHNode(BHTree.BHNode.area_from_node(self, part)))
                getattr(self, part).add_planet(removed_planet)
                getattr(self, part).add_planet(_planet)
            elif isinstance(getattr(self, part), BHTree.BHNode):
                element = getattr(self, part)
                part = element.which_part(_planet)
                if getattr(element, part) is None:
                    setattr(element, part, _planet)
                else:
                    element.add_planet(_planet)
            else:
                setattr(self, part, _planet)

        def may_contain(self, planet):
            if planet.r[0] >= self.area.x and planet.r[0] <= self.area.x + self.area.width and \
                    planet.r[1] >= self.area.y - self.area.width and planet.r[1] <= self.area.y:
                return True
            return False

        def which_part(self, planet):
            if not self.may_contain(planet):
                return None

            if planet.r[0] <= self.area.x+self.area.width/2:
                if planet.r[1] >= self.area.y-self.area.width/2:
                    return 'nw'
                return 'sw'
            else:
                if planet.r[1] >= self.area.y-self.area.width/2:
                    return 'ne'
                return 'se'

        @staticmethod
        def area_from_node(node, direction):
            area = None
            if direction == 'nw':
                area = Area(node.area.x, node.area.y, node.area.width / 2)
            elif direction == 'ne':
                area = Area(node.area.x+node.area.width/2, node.area.y, node.area.width / 2)
            elif direction == 'sw':
                area = Area(node.area.x, node.area.y-node.area.width / 2, node.area.width / 2)
            elif direction == 'se':
                area = Area(node.area.x+node.area.width / 2, node.area.y - node.area.width/2, node.area.width/2)
            return area

        def force_iterator(self, _planet):
            for quarter in 'nw', 'ne', 'sw', 'se':
                xx = getattr(self, quarter)
                if isinstance(xx, BHTree.BHNode):
                    if xx.area.width/xx.mass_center_distance(_planet) < PHI:
                        yield xx
                    else:
                        yield from xx.force_iterator(_planet)
                elif isinstance(xx, planet.Planet):
                    if xx != _planet:
                        yield xx

        def __iter__(self):
            planets_to_yield = []
            nodes_to_yield = []
            for quarter in 'nw', 'ne', 'sw', 'se':
                xx = getattr(self, quarter)
                if isinstance(xx, planet.Planet):
                    planets_to_yield.append(xx)
                elif isinstance(xx, BHTree.BHNode):
                    nodes_to_yield.append(xx)
            yield from planets_to_yield
            yield from nodes_to_yield
            for node in nodes_to_yield:
                yield from node

        def __contains__(self, _planet):
            contains = False
            for element in self:
                if isinstance(element, planet.Planet):
                    if element == _planet:
                        contains = True
            return contains

    def __init__(self, size=(500, 500)):
        self.root = self.BHNode(Area(0, 499, 500))
        self.size = size

    def add_planet(self, planet):
        self.root.add_planet(planet)

    def force_iterator(self, _planet):
        yield from self.root.force_iterator(_planet)

    def __iter__(self):
        yield from self.root

t = BHTree()