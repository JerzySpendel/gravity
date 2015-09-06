import math
from constants import G, STANDARD_PLANET_MASS, COLLISION_DISTANCE
import bhtree
import copy
import constants


class Planet:
    collided = False

    def __init__(self, galaxy, v=None, r=None, mass=None):
        self.v = v or [0, 0]
        self.r = r or [100, 100]
        self.mass = mass or STANDARD_PLANET_MASS
        self.galaxy = galaxy

    @property
    def force(self):
        return self.calculate_force()

    @property
    def acceleration(self):
        f = self.force
        f[0] /= self.mass
        f[1] /= self.mass
        return f

    @property
    def position(self):
        return [int(self.r[0]), int(self.r[1])]

    def distance(self, planet):
        dist = self.distance_vector(planet)
        return math.sqrt(dist[0]**2 + dist[1]**2)

    def distance_vector(self, planet):
        return [planet.r[0] - self.r[0], planet.r[1] - self.r[1]]

    def force_from_planet(self, _planet):
        distance_vector = self.distance_vector(_planet)
        distance_module = self.distance(_planet)
        force_module = constants.G*self.mass*_planet.mass/(distance_module**3)
        return [force_module*distance_vector[0], force_module*distance_vector[1]]

    def force_from_node(self, node):
        _planet = Planet(self.galaxy, r=node.mass_center, mass=node.mass)
        return self.force_from_planet(_planet)

    def calculate_force(self):
        f = [0, 0]
        for element in self.galaxy.planets.force_iterator(self):
            _f = [0, 0]
            if isinstance(element, bhtree.BHTree.BHNode):
                _f = self.force_from_node(element)
            elif isinstance(element, Planet):
                _f = self.force_from_planet(element)
            f[0] += _f[0]
            f[1] += _f[1]
        return f

    def collides(self):
        for other in self.galaxy.planets:
            if isinstance(other, Planet):
                if self.distance(other) <= COLLISION_DISTANCE and self is not other:
                    self.collided = other
                    other.collided = self
                    return True
                self.collided = False

    def handle_collision(self, _planet):
        position = [(_planet.r[0] + self.r[0])/2, (_planet.r[1] + self.r[1])/2]
        velocity = [(_planet.v[0]*_planet.mass + self.v[0]*self.mass)/(self.mass+_planet.mass)
            ,(_planet.v[1]*_planet.mass + self.v[1]*self.mass)/(self.mass+_planet.mass)]
        mass = _planet.mass + self.mass
        return Planet(self.galaxy, r=position, v=velocity, mass=mass)

    def reflect_from_wall_if_needed(self):
        area = self.galaxy.planets.root.area
        if self.r[0] < area.x:
            self.r[0] = area.x
            self.v[0] = -self.v[0]
        elif self.r[0] > area.x + area.width:
            self.r[0] = area.x + area.width
            self.v[0] = -self.v[0]
        elif self.r[1] < area.y - area.width:
            self.r[1] = area.y - area.width
            self.v[1] = -self.v[1]
        elif self.r[1] > area.y:
            self.r[1] = area.y
            self.v[1] = -self.v[1]

    def __eq__(self, other):
        return self.r == other.r and self.mass == other.mass and self.v == other.v

    def __hash__(self):
        return hash('{}:{}:{}'.format(self.r, self.v, self.mass))

    def __str__(self):
        return '<{}: r={},v={},mass={}>'.format('Planet', self.r, self.v, self.mass)