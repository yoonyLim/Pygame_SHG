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
        self.average_distance = sqrt(self.boundary.right * self.boundary.bottom / self.num_particles / 2)
        self.dimension = max(self.average_distance, self.particle_radius)
        self.cells = {}

    def calc_cell_idx(self, position: tuple[int, int]):
        return int(position[0] / self.dimension), int(position[1] / self.dimension)
    
    def add_particle(self, particle: Particle):
        cell_idx = self.calc_cell_idx(particle.position)

        if cell_idx not in self.cells:
            self.cells[cell_idx] = []

        self.cells[cell_idx].append(particle)

    def get_nearby_cells(self, cell_idx: tuple[int, int]):
        return [(cell_idx[0] + dx, cell_idx[1] + dy) for dx in range(-1, 2) for dy in range(-1, 2)]
    
    def get_nearby_particles(self, particle: Particle):
        cell_idx = self.calc_cell_idx(particle.position)
        nearby_particles: List[Particle] = []

        for nearby_cell in self.get_nearby_cells(cell_idx):
            if nearby_cell in self.cells:
                nearby_particles.extend([other_particle for other_particle in self.cells[nearby_cell] if other_particle != particle])

        return nearby_particles