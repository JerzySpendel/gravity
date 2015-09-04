import math
import copy
import random
import pygame
import sys
from gameclock import GameClock

G = 1


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


class Galaxy:
    def __init__(self, planets=None):
        if planets is None:
            planets = []
            for i in range(5):
                planet1 = Planet(self, r=[200+i*20, 200], v=[5, 0])
                planet2 = Planet(self, r=[200+i*20, 210], v=[-5, 0])
                planets.extend([planet1, planet2])
            self.planets = planets
        else:
            self.planets = planets

    def add_random_planets(self, n):
        x_margin = 200
        y_margin = 200
        gap = 10
        for x in range(x_margin, x_margin+n*gap, gap):
            for y in range(y_margin, y_margin+n*gap, gap):
                self.planets.append(Planet(self, r=[x, y]))

    def apply_dt(self, dt):
        planets = []
        to_remove = set()
        to_append = set()
        for planet in self.planets:
            _to_remove, _to_append = planet.check_for_collision()
            to_remove.update(_to_remove)
            to_append.update(_to_append)
        for planet in to_remove:
            self.planets.remove(planet)
        self.planets.extend(to_append)
        if len(to_append) != 0:
            print(to_append)

        for planet in self.planets:
            planet = copy.copy(planet)
            dx, dy = planet.v[0]*dt, planet.v[1]*dt
            planet.r[0] += dx
            planet.r[1] += dy
            acceleration = planet.acceleration
            planet.v[0] += acceleration[0]*dt
            planet.v[1] += acceleration[1]*dt
            planets.append(planet)
        self.planets = planets


class GalaxyView:
    def __init__(self):
        self.galaxy = Galaxy()
        self.screen = pygame.display.set_mode((500, 500))
        self.clock = GameClock(200, update_callback=self.update)

    def draw_planets(self):
        for planet in self.galaxy.planets:
            self.screen.set_at(planet.position, (255, 255, 255))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_planets()
        pygame.display.flip()

    def main_loop(self):
        while True:
            self.clock.tick()

    def update(self, dt):
        self.galaxy.apply_dt(dt)
        self.draw()

v = GalaxyView()
v.main_loop()
