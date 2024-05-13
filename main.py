import simpleaudio as sa
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from particles import Particle
from music import generate_note, key_to_note


def main():
    pygame.init()
    particles = []
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    running = True
    keys_being_pressed = {}
    note_generators = {}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in key_to_note and event.key not in keys_being_pressed:
                    # Start generating the note for this key
                    current_note = key_to_note[event.key]
                    keys_being_pressed[event.key] = current_note
                    # Generate a 2-second note
                    note_samples = generate_note(current_note, duration=2)
                    note_generators[event.key] = sa.play_buffer(
                        note_samples, 1, 2, 44100)
                    # Create a new particle system for the note
                    particles.append(Particle(0, 0, 0, current_note))
            elif event.type == pygame.KEYUP:
                if event.key in keys_being_pressed:
                    # Stop generating the note for this key
                    del keys_being_pressed[event.key]
                    # Don't stop the note immediately, let it continue playing until the end of the fade-out period
                    # Set a timer to fire an event after 1 second
                    pygame.time.set_timer(pygame.USEREVENT, 1000)
                    note_to_stop = event.key  # Remember which note to stop

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Update and draw all particles
        [p.move() for p in particles]
        [p.draw() for p in particles]

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()
    quit()


main()
