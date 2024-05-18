"""
This module initializes an OpenGL window using Pygame and handles
keyboard inputs to play musical notes and create visual effects with particles.
It utilizes the simpleaudio library for sound generation and playback,
and custom modules for musical notes and color mappings.
"""

import simpleaudio as sa
import pygame
from music.graphics.particles import Particle, render_scene
from music.music import generate_and_play_note
from music.graphics.notes_color import key_to_note
from music.graphics.init import init_pygame


def handle_keydown(event, keys_being_pressed, note_generators, particles):
    """Handles keydown events to play notes and generate particles."""
    if event.key in key_to_note and event.key not in keys_being_pressed:
        play_note(event, keys_being_pressed, note_generators)
        particles.append(Particle(0, 0, 0, key_to_note[event.key]))


def play_note(event, keys_being_pressed, note_generators):
    """Generates and plays a note based on the key pressed."""
    current_note = [key_to_note[event.key]]
    keys_being_pressed[event.key] = current_note
    note_settings = {
        "attack_time": 0.1,
        "decay_time": 0.1,
        "release_time": 0.1,
        "duration": 0.7
    }
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        note_settings["duration"] *= 2
    note_samples = generate_and_play_note(
        current_note[0], **note_settings)
    note_generators[event.key] = sa.play_buffer(note_samples, 1, 2, 44100)


def handle_keyup(event, keys_being_pressed):
    """Cleans up resources after a key is released."""
    if event.key in keys_being_pressed:
        del keys_being_pressed[event.key]
        pygame.time.set_timer(pygame.USEREVENT, 1000)


def main_loop():
    """Main loop for handling events and rendering the scene."""
    display = (600, 600)
    init_pygame(display)
    particles = []
    running = True
    keys_being_pressed = {}
    note_generators = {}
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keydown(event, keys_being_pressed,
                               note_generators, particles)
            elif event.type == pygame.KEYUP:
                handle_keyup(event, keys_being_pressed)
        render_scene(particles)
    pygame.quit()


if __name__ == "__main__":
    main_loop()
