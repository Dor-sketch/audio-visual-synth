"""
This script defines a Particle class that represents a group of particles moving in a 3D space.
The particles are rendered as spheres using PyOpenGL and Pygame. The Particle class has methods
to update the position of the particles, draw them, and create visual effects like smoke trails.
The script also demonstrates how to create a simple scene with multiple particles
moving in different directions.
"""

import random
import numpy as np
import pygame
from .notes_color import note_to_color
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pygame.locals import *


def update_particles(particles):
    """Updates and renders particles."""
    for particle in particles:
        particle.move()
        particle.draw()

def render_scene(particles):
    """Renders the OpenGL scene."""
    glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    update_particles(particles)
    pygame.display.flip()
    pygame.time.wait(10)

class Particle:
    VELOCITY_STD_DEV = 0.001
    VELOCITY_CHANGE_STD_DEV = 0.1
    POSITION_STD_DEV = 0.05
    ALPHA_DECAY_RATE = 0.0005
    UPWARD_BIAS = 0.002
    SHRINK_RATE = 0.0005
    # Define the vertices of the pyramids
    # Define the sides of the pyramids
    UPWARD_PYRAMID_SIDES = np.array(
        [
            [[0, 0, 1], [1, 0, 0]],
            [[0, 0, 1], [-0.5, np.sqrt(3) / 2, 0]],
            [[0, 0, 1], [-0.5, -np.sqrt(3) / 2, 0]],
            [[1, 0, 0], [-0.5, np.sqrt(3) / 2, 0]],
            [[1, 0, 0], [-0.5, -np.sqrt(3) / 2, 0]],
            [[1, 0, 0], [0, 0, 1]],
            [[-0.5, np.sqrt(3) / 2, 0], [-0.5, -np.sqrt(3) / 2, 0]],
            [[-0.5, -np.sqrt(3) / 2, 0], [1, 0, 0]],
            [[-0.5, np.sqrt(3) / 2, 0], [1, 0, 0]],
        ]
    )

    DOWNWARD_PYRAMID_SIDES = np.array(
        [
            [[0, 0, -1], [-1, 0, 0]],
            [[0, 0, -1], [0.5, -np.sqrt(3) / 2, 0]],
            [[0, 0, -1], [0.5, np.sqrt(3) / 2, 0]],
            [[-1, 0, 0], [0.5, -np.sqrt(3) / 2, 0]],
            [[-1, 0, 0], [0.5, np.sqrt(3) / 2, 0]],
            [[-1, 0, 0], [0, 0, -1]],
            [[0.5, -np.sqrt(3) / 2, 0], [0.5, np.sqrt(3) / 2, 0]],
            [[0.5, np.sqrt(3) / 2, 0], [-1, 0, 0]],
            [[0.5, -np.sqrt(3) / 2, 0], [-1, 0, 0]],
        ]
    )
    # Initialize the last assigned side index
    last_side_index = 0

    def __init__(self, x, y, z, note):
        num_particles = random.randint(20, 30)
        self.particles = []
        for i in range(num_particles):
            position = np.array([x, y, z], dtype=np.float64) + np.random.normal(
                0, self.POSITION_STD_DEV, 3
            )
            velocity = np.random.normal(0, self.VELOCITY_STD_DEV, 3)
            # Add upward bias to the y component of velocity
            velocity[1] += self.UPWARD_BIAS
            # Assign each particle to a side of the pyramids
            if Particle.last_side_index % 2 == 0:
                side = self.UPWARD_PYRAMID_SIDES[
                    Particle.last_side_index % len(self.UPWARD_PYRAMID_SIDES)
                ]
            else:
                side = self.DOWNWARD_PYRAMID_SIDES[
                    Particle.last_side_index % len(self.DOWNWARD_PYRAMID_SIDES)
                ]
            # Choose a random point on the side
            t = np.random.uniform(0, 1)
            target = side[0] * (1 - t) + side[1] * t
            self.particles.append(
                {
                    "position": position,
                    "velocity": velocity,
                    "alpha": 0.5,
                    "size": 0.07,
                    "target": target,
                }
            )
            # Increment the last assigned side index
            Particle.last_side_index += 1
        if isinstance(note, list):
            self.note = note[0]
        else:
            self.note = note

    def move(self):
        for particle in self.particles:
            # The target point is already set in the particle's target
            target_point = particle["target"]

            # Check if the particle has reached its target
            if (
                np.linalg.norm(target_point - particle["position"])
                > self.VELOCITY_CHANGE_STD_DEV
            ):
                # Calculate the direction to the target
                direction = target_point - particle["position"]
                # Normalize the direction
                direction /= np.linalg.norm(direction)
                # Update the particle's position by moving a small step in the direction of the target
                particle["position"] += direction * self.VELOCITY_CHANGE_STD_DEV

            particle["alpha"] -= self.ALPHA_DECAY_RATE
            # Decrease size to create a smoke-like effect
            particle["size"] -= self.SHRINK_RATE

    def move2(self):
        for particle in self.particles:
            # Calculate the direction to the target
            direction = particle["target"] - particle["position"]
            # Normalize the direction
            direction /= np.linalg.norm(direction)
            # Adjust the velocity towards the target
            # Add a small threshold to prevent overshooting
            if np.linalg.norm(particle["position"] - particle["target"]) > 0.1:
                particle["velocity"] += direction * self.VELOCITY_CHANGE_STD_DEV
            else:
                # Stop moving once the target is reached
                particle["velocity"] = np.zeros(3)

            if not np.all(np.abs(particle["position"]) <= 50):
                particle["position"] = np.random.normal(0, self.POSITION_STD_DEV, 3)

    def draw(self):
        for particle in self.particles:
            glColor4fv((*note_to_color.get(self.note, (1, 1, 1)), particle["alpha"]))
            glPushMatrix()
            glTranslatef(*particle["position"])
            # Use self.size instead of a magic number
            glutSolidSphere(particle["size"], 20, 20)
            glPopMatrix()


if __name__ == "__main__":
    """
    Main function to display the particles in a 3D scene.
    """
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    running = True
    # Initialize particles along two lines
    particles = []
    for i in range(10):
        particles.append(Particle(-5 + i, 0, 0, "C4"))
        particles.append(Particle(-5 + i, 1, 0, "D4"))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Update and draw all particles
        [p.move2() for p in particles]
        [p.draw() for p in particles]

        pygame.display.flip()
        # Wait a short amount of time to limit the frame rate
        pygame.time.wait(10)

    pygame.quit()
