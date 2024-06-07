import asyncio
import pygame
from pygame.locals import *
import numpy as np

# Note to MIDI and color mappings
note_to_midi = {
    "C3": 48, "C#3": 49, "D3": 50, "D#3": 51, "E3": 52, "F3": 53, "F#3": 54,
    "G3": 55, "G#3": 56, "A3": 57, "A#3": 58, "B3": 59,
    "C4": 60, "C#4": 61, "D4": 62, "D#4": 63, "E4": 64, "F4": 65, "F#4": 66,
    "G4": 67, "G#4": 68, "A4": 69, "A#4": 70, "B4": 71, "C5": 72, "C#5": 73,
    "D5": 74, "D#5": 75, "E5": 76, "F5": 77, "F#5": 78, "G5": 79, "G#5": 80,
}

note_to_color = {
    48: (0, 0, 255), 49: (0, 100, 255), 50: (0, 200, 255), 51: (0, 255, 200),
    52: (0, 255, 100), 53: (0, 255, 0), 54: (100, 255, 0), 55: (200, 255, 0),
    56: (255, 200, 0), 57: (255, 100, 0), 58: (255, 0, 0), 59: (255, 0, 100),
    60: (0, 0, 255), 61: (0, 100, 255), 62: (0, 200, 255), 63: (0, 255, 200),
    64: (0, 255, 100), 65: (0, 255, 0), 66: (100, 255, 0), 67: (200, 255, 0),
    68: (255, 200, 0), 69: (255, 100, 0), 70: (255, 0, 0), 71: (255, 0, 100),
    72: (255, 0, 200), 73: (255, 0, 255), 74: (200, 0, 255), 75: (100, 0, 255),
    76: (0, 0, 255), 77: (0, 100, 255), 78: (0, 200, 255), 79: (0, 255, 200),
    80: (0, 255, 100)
}

key_to_note = {
    pygame.K_z: 48, pygame.K_x: 50,
    pygame.K_c: 52, pygame.K_v: 53, pygame.K_b: 55,
    pygame.K_n: 57, pygame.K_m: 59, pygame.K_COMMA: 60, pygame.K_q: 59,
    pygame.K_a: 60, pygame.K_w: 61, pygame.K_s: 62, pygame.K_e: 63,
    pygame.K_d: 64, pygame.K_f: 65, pygame.K_t: 66, pygame.K_g: 67,
    pygame.K_y: 68, pygame.K_h: 69, pygame.K_u: 70, pygame.K_j: 71,
    pygame.K_k: 72, pygame.K_o: 73, pygame.K_l: 74, pygame.K_p: 75,
    pygame.K_SEMICOLON: 76, pygame.K_LEFTBRACKET: 77, pygame.K_QUOTE: 77,
    pygame.K_RIGHTBRACKET: 78, pygame.K_BACKSLASH: 80, pygame.K_RETURN: 79,
    pygame.K_SPACE: 48
}

import random
# Particle class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(5, 12)  # Randomize initial size
        self.speed = random.uniform(1.5, 2.5)  # Increase speed range for swifter movement
        self.alpha = 255  # Initial transparency

    def move(self):
        self.y -= self.speed  # Use speed for movement
        self.alpha = max(0, min(255, int(self.alpha - 1)))  # Decrease transparency more slowly for longer lasting particles

    def draw(self, screen):
        if self.size > 0:  # Only draw the particle if it hasn't faded out
            surface = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)  # Create a new surface with alpha channel
            pygame.draw.circle(surface, self.color + (self.alpha,), (self.size, self.size), self.size)  # Draw the particle on the surface
            screen.blit(surface, (self.x - self.size, self.y - self.size))  # Blit the surface onto the screen
def init_pygame(display=(800, 600)):
    pygame.init()
    pygame.display.set_mode(display)
    pygame.display.set_caption("Pygame Music Visualizer")
    #high framerate
    pygame.time.set_timer(pygame.USEREVENT, 1000 // 60)
    #high fps
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // 60)

def generate_wave(note, duration=1.0, volume=0.5, sample_rate=44100):
    frequency = 440 * 2 ** ((note - 69) / 12)
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Creating an ADSR envelope
    attack_time = 0.01
    decay_time = 0.1
    sustain_level = 0.7
    release_time = 0.2
    sustain_time = duration - attack_time - decay_time - release_time

    envelope = np.concatenate([
        np.linspace(0, 1, int(sample_rate * attack_time)),  # Attack
        np.linspace(1, sustain_level, int(sample_rate * decay_time)),  # Decay
        np.full(int(sample_rate * sustain_time), sustain_level),  # Sustain
        np.linspace(sustain_level, 0, int(sample_rate * release_time))  # Release
    ])

    # Ensure the envelope matches the length of the sound wave
    envelope = np.pad(envelope, (0, max(0, len(t) - len(envelope))), 'constant')

    wave = 0.5 * np.sin(frequency * 2 * np.pi * t) * envelope * volume
    return (wave * 32767).astype(np.int16)

def play_wave(note, duration=1.0, volume=0.5, sample_rate=44100):
    wave = generate_wave(note, duration, volume, sample_rate)
    stereo_wave = np.zeros((wave.size, 2), dtype=np.int16)
    stereo_wave[:, 0] = wave
    stereo_wave[:, 1] = wave

    pygame.mixer.init(sample_rate, -16, 2)
    wave_bytes = stereo_wave.tobytes()
    sound = pygame.mixer.Sound(buffer=wave_bytes)
    sound.play()

async def handle_keydown(event, keys_being_pressed, particles, key_positions):
    if event.key in key_to_note and event.key not in keys_being_pressed:
        current_note = key_to_note[event.key]
        keys_being_pressed[event.key] = current_note
        color = note_to_color.get(current_note, (255, 255, 255))
        position = key_positions[current_note]
        particles.append(Particle(position[0], position[1], color))
        play_wave(current_note)

async def handle_keyup(event, keys_being_pressed):
    if event.key in keys_being_pressed:
        del keys_being_pressed[event.key]

def render_scene(screen, particles):
    screen.fill((0, 0, 0))
    for particle in particles:
        particle.move()
        particle.draw(screen)
    pygame.display.flip()

def calculate_key_positions(display_width, display_height):
    key_positions = {}
    num_keys = len(note_to_color)
    key_width = display_width // num_keys
    for note in note_to_color:
        octave = (note // 12) - 4
        x = (((note % num_keys) * key_width + key_width // 2) - 350 ) % display_width
        y = display_height - (octave + 1) * 50
        key_positions[note] = (x, y)
    return key_positions

async def main_loop():
    display = (800, 600)
    init_pygame(display)
    screen = pygame.display.get_surface()
    particles = []
    running = True
    keys_being_pressed = {}
    key_positions = calculate_key_positions(display[0], display[1])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                await handle_keydown(event, keys_being_pressed, particles, key_positions)
            elif event.type == pygame.KEYUP:
                await handle_keyup(event, keys_being_pressed)

        render_scene(screen, particles)
        await asyncio.sleep(0)

    pygame.quit()

# This is the program entry point:
asyncio.run(main_loop())