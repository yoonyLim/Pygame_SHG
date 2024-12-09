from math import sqrt
from typing import List
import pygame as pg
import content.simulation_manger as sim
from content.physics.particle import Particle

class SpatialHashGrid:
    def __init__(self, boundary: pg.Rect, num_particles: int, particle_radius: float):
        self.boundary = boundary
        self.num_particles = num_particles
        self.particle_radius = particle_radius
        self.average_distance = sqrt(self.boundary.right * self.boundary.bottom / (self.num_particles / 2))
        self.dimension = max(self.average_distance, self.particle_radius)
        self.grids = {}

    def get_hash(self, position: tuple[int, int]):
        return int(position[0] / self.dimension), int(position[1] / self.dimension)
    
    def add_particle(self, particle: Particle):
        grid_hash = self.get_hash(particle.position)

        if grid_hash not in self.grids:
            self.grids[grid_hash] = []

        self.grids[grid_hash].append(particle)

    def get_nearby_grids(self, grid_hash: tuple[int, int]):
        return [(grid_hash[0] + dx, grid_hash[1] + dy) for dx in range(-1, 2) for dy in range(-1, 2)]
    
    def get_nearby_particles(self, particle: Particle):
        grid_hash = self.get_hash(particle.position)
        nearby_particles: List[Particle] = []

        for nearby_grid in self.get_nearby_grids(grid_hash):
            if nearby_grid in self.grids:
                nearby_particles.extend([other_particle for other_particle in self.grids[nearby_grid] if other_particle != particle])

        return nearby_particles