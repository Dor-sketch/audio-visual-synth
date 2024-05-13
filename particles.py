import random
from shapes import STAR_OF_DAVID_VERTICES
import numpy as np
from notes_color import key_to_note, note_to_color
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pygame.locals import *


class Particle:
    VELOCITY_STD_DEV = 0.0001
    VELOCITY_CHANGE_STD_DEV = 0.00001
    POSITION_STD_DEV = 0.5
    ALPHA_DECAY_RATE = 0.0005

    UPWARD_BIAS = 0.0002  # Make particles move upwards more than in other directions
    SHRINK_RATE = 0.0005  # Make particles shrink over time

    def __init__(self, x, y, z, note):
        num_particles = random.randint(10, 20)
        self.particles = []
        for _ in range(num_particles):
            position = np.array([x, y, z], dtype=np.float64) + \
                np.random.normal(0, self.POSITION_STD_DEV, 3)
            velocity = np.random.normal(0, self.VELOCITY_STD_DEV, 3)
            # Add upward bias to the y component of velocity
            velocity[1] += self.UPWARD_BIAS
            # Choose a random vertex of the Star of David as the target
            target = random.choice(STAR_OF_DAVID_VERTICES)
            self.particles.append({
                'position': position,
                'velocity': velocity,
                'alpha': 0.5,
                'size': 0.07,
                'target': target,
            })
        self.note = note

    def move(self):
        for particle in self.particles:
            # Calculate the direction to the target
            direction = particle['target'] - particle['position']
            # Normalize the direction
            direction /= np.linalg.norm(direction)
            # Adjust the velocity towards the target
            particle['velocity'] += direction * self.VELOCITY_CHANGE_STD_DEV

            if not np.all(np.abs(particle['position']) <= 50):
                particle['position'] = np.random.normal(
                    0, self.POSITION_STD_DEV, 3)

            particle['alpha'] -= self.ALPHA_DECAY_RATE
            # Decrease size to create a smoke-like effect
            particle['size'] -= self.SHRINK_RATE

    def move2(self):
        for particle in self.particles:
            # Calculate the direction to the target
            direction = particle['target'] - particle['position']
            # Normalize the direction
            direction /= np.linalg.norm(direction)
            # Adjust the velocity towards the target
            if np.linalg.norm(particle['position'] - particle['target']) > 0.1:  # Add a small threshold to prevent overshooting
                particle['velocity'] += direction * self.VELOCITY_CHANGE_STD_DEV
            else:
                particle['velocity'] = np.zeros(3)  # Stop moving once the target is reached

            if not np.all(np.abs(particle['position']) <= 50):
                particle['position'] = np.random.normal(
                    0, self.POSITION_STD_DEV, 3)

    def draw(self):
        for particle in self.particles:
            glColor4fv(
                (*note_to_color.get(self.note, (1, 1, 1)), particle['alpha']))
            glPushMatrix()
            glTranslatef(*particle['position'])
            # Use self.size instead of a magic number
            glutSolidSphere(particle['size'], 20, 20)
            glPopMatrix()


if __name__ == '__main__':
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    running = True
    # Initialize particles along two lines
    particles = [Particle(0, 0, 0, 60)]
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
