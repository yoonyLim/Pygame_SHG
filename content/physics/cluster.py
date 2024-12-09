import random
from typing import List
import pygame as pg
import content.simulation_manger as sim
from content.physics.particle import Particle
from content.physics.spatial_hash_grid import SpatialHashGrid

class Cluster:
    def __init__(self, boundary: pg.Rect, num_particles: int, energy_loss: float = sim.ENERGY_LOSS, gravity: float = sim.GRAVITY):
        self.boundary = boundary
        self.num_particles = num_particles
        self.particles: List[Particle] = []
        self.energy_loss = energy_loss
        self.gravity = gravity

        for i in range(self.num_particles):
            new_particle = Particle(
                random.uniform(0, self.boundary.right - 1), 
                random.uniform(self.boundary.bottom / 2, self.boundary.bottom - 1), 
                0.0, 
                0.0, 
                sim.MASS, 
                sim.RADIUS)
            self.particles.append(new_particle)

    def draw(self, screen: pg.Surface):
        for particle in self.particles:
            pg.draw.circle(screen, particle.color, (int(particle.position[0]), int(particle.position[1])), particle.radius)

            surface = pg.Surface((particle.radius * 2, particle.radius * 2), pg.SRCALPHA)
            surface.fill((0, 0, 0, 0))

            pg.draw.circle(surface, particle.color, (particle.radius, particle.radius), particle.radius)

            screen.blit(surface, (int(particle.position[0] - particle.radius), int(particle.position[1] - particle.radius)))

    def update(self):
        for i, particle in enumerate(self.particles):
            particle.density = 0

            for j, other_particle in enumerate(self.particles):
                if i != j:
                    distance, direction = particle.get_distance_direction(other_particle)

                    if distance < particle.radius + other_particle.radius:
                        particle.update_collision(other_particle, distance, direction, self.energy_loss)

        for particle in self.particles:
            particle.update_position(self.boundary, self.gravity, self.energy_loss)

    def update_SPH(self):
        self.SHG = SpatialHashGrid(self.boundary, self.num_particles, sim.RADIUS)

        for particle in self.particles:
            self.SHG.add_particle(particle)
            nearby_particles = self.SHG.get_nearby_particles(particle)

            for other_particle in nearby_particles:
                distance, direction = particle.get_distance_direction(other_particle)

                if distance < particle.radius + other_particle.radius:
                    particle.update_collision(other_particle, distance, direction, self.energy_loss)

        for particle in self.particles:
            particle.update_position(self.boundary, self.gravity, self.energy_loss)