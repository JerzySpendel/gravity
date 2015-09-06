from gameclock import GameClock
from constants import FPS
import bhtree
import pygame
import copy
import sys
import planet
import random


class Galaxy:
    def __init__(self, planets=None):
        self.planets = bhtree.BHTree()
        self.add_random(300)

    def add_random(self, n):
        for _ in range(n):
            self.planets.add_planet(planet.Planet(self, r=[random.randint(0,500), random.randint(0,500)]))

    def apply_dt(self, dt):
        new_planets = bhtree.BHTree()
        for _planet in self.planets:
            if isinstance(_planet, planet.Planet):
                _planet.collides()
                if _planet.collided:
                    new_planet = _planet.handle_collision(_planet.collided)
                    new_planets.add_planet(new_planet)
                elif not _planet.collided:
                    new_planets.add_planet(_planet)
        self.planets = new_planets
        new_planets = bhtree.BHTree()
        for _planet in self.planets:
            if isinstance(_planet, planet.Planet):
                _planet = copy.copy(_planet)
                dx, dy = _planet.v[0]*dt, _planet.v[1]*dt
                _planet.r[0] += dx
                _planet.r[1] += dy
                acceleration = _planet.acceleration
                _planet.v[0] += acceleration[0]*dt
                _planet.v[1] += acceleration[1]*dt
                _planet.reflect_from_wall_if_needed()
                new_planets.add_planet(_planet)
        self.planets = new_planets

    def add_planet(self, _planet):
        self.planets.add_planet(_planet)


class GalaxyView:
    def __init__(self):
        self.galaxy = Galaxy()
        self.screen = pygame.display.set_mode((500, 500))
        self.clock = GameClock(FPS, update_callback=self.update)

    def draw_planets(self):
        for _planet in self.galaxy.planets:
            if isinstance(_planet, planet.Planet):
                self.screen.set_at(_planet.position, (255, 255, 255))

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

g = GalaxyView()
