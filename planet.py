import math
from constants import G
import copy


class Planet:
    def __init__(self, galaxy, v=None, r=None, mass=None):
        self.v = v or [0, 0]
        self.r = r or [100, 100]
        self.mass = mass or 1000
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

    def calculate_force(self):
        f = [0, 0]
        planets = copy.copy(self.galaxy.planets)
        planets.remove(self)
        for planet in planets:
            force_module = G*self.mass*planet.mass/(self.distance(planet)**3)
            distance_vector = self.distance_vector(planet)
            force_vector = [distance_vector[0]*force_module, distance_vector[1]*force_module]
            f[0] += force_vector[0]
            f[1] += force_vector[1]
        return f

    def collides(self, other):
        if other.position == self.position and self is not other:
            return True
        return False

    def check_for_collision(self):
        to_append = set()
        to_remove = set()
        for planet in self.galaxy.planets:
            if self.collides(planet):
                to_remove.update({self, planet})
                position = [(planet.r[0] + self.r[0])/2, (planet.r[1] + self.r[1])/2]
                velocity = [(planet.v[0] + self.v[0])/2, (planet.v[1] + self.v[1])/2]
                mass = planet.mass + self.mass
                to_append.add(Planet(self.galaxy, r=position, v=velocity, mass=mass))
        return to_remove, to_append

    def __eq__(self, other):
        return self.r == other.r and self.mass == other.mass and self.v == other.v

    def __hash__(self):
        return hash('{}:{}:{}'.format(self.r, self.v, self.mass))