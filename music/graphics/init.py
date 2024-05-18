"""
This module initializes the pygame display with OpenGL settings.
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def init_pygame(display=None):
    """Initializes the pygame display with OpenGL settings."""
    if display is None:
        display = (600, 600)
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
