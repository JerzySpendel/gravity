from gameclock import GameClock
from planet import Planet
import pygame
import copy
import sys


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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()