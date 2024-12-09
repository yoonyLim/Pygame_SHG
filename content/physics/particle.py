from math import sqrt, pi
import numpy as np
import pygame as pg
import content.simulation_manger as sim

class Particle:
    def __init__(self, x_pos: float, y_pos: float, x_vel: float = 0.0, y_vel: float = 0.0, mass: float = 1.0, radius: float = 1.0, color = (255, 255, 255, 255)):
        self.position = np.array([x_pos, y_pos])
        self.velocity = np.array([x_vel, y_vel])
        self.mass = mass
        self.radius = radius
        self.color = color

    def update_position(self, boundary: pg.Rect, gravity: float = sim.GRAVITY, energy_loss: float = sim.ENERGY_LOSS):
        # planet like attracts particles to the center to form a planet-like shape
        if sim.PLANET_LIKE:
            center_delta = np.array(sim.PLANET_CENTER) - self.position
            center_distance = sqrt(center_delta[0] ** 2 + center_delta[1] ** 2)
            center_direction = np.array([center_delta[0] / (center_distance + 1e-8), center_delta[1] / (center_distance + 1e-8)])
            self.velocity += center_direction * sim.ENERGY_LOSS
        elif gravity > 0:
            self.velocity[1] += gravity / 3

        self.position += self.velocity / 3

        if self.position[0] - self.radius <= boundary.left:
            self.position[0] = boundary.left + self.radius
            self.velocity[0] = -self.velocity[0] * energy_loss
        elif self.position[0] + self.radius >= boundary.right:
            self.position[0] = boundary.right - self.radius
            self.velocity[0] = -self.velocity[0] * energy_loss

        if self.position[1] - self.radius <= boundary.top:
            self.position[1] = boundary.top + self.radius
            self.velocity[1] = -self.velocity[1] * energy_loss
        elif self.position[1] + self.radius >= boundary.bottom:
            self.position[1] = boundary.bottom - self.radius
            self.velocity[1] = -self.velocity[1] * energy_loss

        # set red for bigger velocity magnitude
        vel_magnitude = self.velocity[0] ** 2 + self.velocity[1] ** 2
        impact = min(vel_magnitude, 2000) / 2000 * 255
        self.color = (int(impact), 255 - int(impact), 255 - int(impact), int(impact))

    def get_distance_direction(self, other_particle):
        pos_delta = self.position - other_particle.position
        distance = sqrt(pos_delta[0] ** 2 + pos_delta[1] ** 2)
        direction = np.array([pos_delta[0] / (distance + 1e-8), pos_delta[1] /(distance + 1e-8)])

        return distance, direction

    def update_collision(self, other_particle, distance: float, direction, energy_loss: float = sim.ENERGY_LOSS):
        if distance <= (self.radius + other_particle.radius):
            vel_normal = np.dot(self.velocity - other_particle.velocity, direction)        

            if vel_normal <= 0:
                impulse = - (1 + energy_loss) * vel_normal / (1 / self.mass + 1 / other_particle.mass) * direction

                self.velocity += impulse / self.mass
                other_particle.velocity -= impulse / other_particle.mass
                
                correction = max(0, self.radius + other_particle.radius - distance) * direction
                self.position += correction / 2
                other_particle.position -= correction / 2