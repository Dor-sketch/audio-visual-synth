"""
This script demonstrates how to render two intersecting tetrahedrons using PyOpenGL.
The script uses the OpenGL library to render the tetrahedrons and Pygame to create
the window and handle events.
The tetrahedrons are defined by their vertices and triangles, and the script uses
the glBegin and glEnd functions to draw the triangles.
The script also sets up a basic scene with a black background and rotates the tetrahedrons around the x and y axes.
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Define the vertices for two intersecting tetrahedrons
UPWARD_PYRAMID_VERTICES = np.array(
    [
        [1, 0, -1 / np.sqrt(2)],
        [-1, 0, -1 / np.sqrt(2)],
        [0, 1, 1 / np.sqrt(2)],
        [0, -1, 1 / np.sqrt(2)],
    ]
)

DOWNWARD_PYRAMID_VERTICES = np.array(
    [
        [1, 0, 1 / np.sqrt(2)],
        [-1, 0, 1 / np.sqrt(2)],
        [0, 1, -1 / np.sqrt(2)],
        [0, -1, -1 / np.sqrt(2)],
    ]
)

# Define the triangles for each pyramid
TRIANGLES = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]


def draw_pyramid(vertices):
    glBegin(GL_TRIANGLES)
    for triangle in TRIANGLES:
        for vertex in triangle:
            glVertex3fv(vertices[vertex])
    glEnd()


def setup_scene():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    setup_scene()

    clock = pygame.time.Clock()
    angle = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(angle, 1, 1, 0)  # Rotate around x and y axes
        glColor3f(1, 0, 0)  # Red color for the first pyramid
        draw_pyramid(UPWARD_PYRAMID_VERTICES)
        glColor3f(0, 0, 1)  # Blue color for the second pyramid
        draw_pyramid(DOWNWARD_PYRAMID_VERTICES)
        glPopMatrix()

        angle += 1  # Increment the angle for rotation
        pygame.display.flip()
        clock.tick(60)  # Limit frames per second to 60

    pygame.quit()


if __name__ == "__main__":
    main()
