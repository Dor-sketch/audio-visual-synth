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
            surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)  # Create a new surface with alpha channel
            pygame.draw.circle(surface, self.color + (self.alpha,), (self.size, self.size), self.size)  # Draw the particle on the surface
            screen.blit(surface, (self.x - self.size, self.y - self.size))  # Blit the surface onto the screen

def init_pygame(display=(1600, 900)):
    pygame.init()
    pygame.display.set_mode(display)
    pygame.display.set_caption("Pygame Music Visualizer")
    pygame.time.set_timer(pygame.USEREVENT, 1000 // 60)

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

def render_scene(screen, particles, key_positions, keys_being_pressed):
    screen.fill((30, 30, 30))
    draw_piano_keys(screen, key_positions, keys_being_pressed)
    for particle in particles:
        particle.move()
        particle.draw(screen)
    pygame.display.flip()

def draw_piano_keys(screen, key_positions, keys_being_pressed):
    white_keys = [note for note in key_positions if note % 12 in [0, 2, 4, 5, 7, 9, 11]]
    key_width = screen.get_width() // len(white_keys)

    for note, (x, y) in key_positions.items():
        color = note_to_color.get(note, (255, 255, 255))
        key_rect = pygame.Rect(x - key_width // 2, y - 100, key_width, 100)
        if note in keys_being_pressed.values():
            # if key is black draw black color
            if note % 12 in [1, 3, 6, 8, 10]:
                pygame.draw.rect(screen, (0, 0, 0), key_rect)
            else:
                pygame.draw.rect(screen, (255, 255, 255), key_rect)
        # if black key draw darker color
        if note % 12 in [1, 3, 6, 8, 10]:
            color = tuple(int(c * 0.8) for c in color)
        pygame.draw.rect(screen, color, key_rect, 5)

def calculate_key_positions(display_width, display_height, note_to_color=note_to_color):
    key_positions = {}
    white_keys = [note for note in note_to_color if note % 12 in [0, 2, 4, 5, 7, 9, 11]]
    white_key_width = display_width // len(white_keys)
    black_key_width = int(white_key_width * 0.6)
    black_key_height = 100

    white_key_index = 0
    for note in sorted(note_to_color.keys()):
        if note % 12 in [0, 2, 4, 5, 7, 9, 11]:
            x = white_key_index * white_key_width
            key_positions[note] = (x + white_key_width // 2, display_height - 150)
            white_key_index += 1
        elif note % 12 in [1, 3, 6, 8, 10]:
            # Position black keys between the white keys, without extra space
            prev_white_key_x = (white_key_index - 1) * white_key_width
            x = prev_white_key_x + (white_key_width - black_key_width // 2)
            key_positions[note] = (x, display_height - 150 - black_key_height)

    return key_positions
async def main_loop():
    display = (800, 800 // 16 * 9)
    init_pygame(display)
    screen = pygame.display.get_surface()
    particles = []
    running = True
    keys_being_pressed = {}
    key_positions = calculate_key_positions(display[0], display[1])
    key_width = display[0] // len(note_to_color)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                await handle_keydown(event, keys_being_pressed, particles, key_positions)
            elif event.type == pygame.KEYUP:
                await handle_keyup(event, keys_being_pressed)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                note = mouse_x // key_width + 48  # Calculate the base note assuming it's a white key
                black_key_height = display[1] - 150 - 100  # Height of the black keys
                # Determine if the note is a black key based on its position in the scale
                if note % 12 in [1, 3, 6, 8, 10]:  # These are the positions of black keys in an octave
                    # Check if the mouse click was within the height range of black keys
                    if mouse_y <= black_key_height:
                        # It's a black key, and the click was within the black key's height
                        pass  # The note is correctly set
                    else:
                        # The click was outside the black key's height, adjust the note for a white key
                        # This logic might need adjustment based on the specific layout of your piano keys
                        note -= 1 if note % 12 in [1, 3] else 1
                # If the note is not a black key, no adjustment is needed based on mouse_y

                if note in key_positions:
                    keys_being_pressed[0] = note
                    x, y = key_positions[note]
                    color = note_to_color.get(note, (255, 255, 255))
                    particles.append(Particle(x, y, color))
                    play_wave(note)
        render_scene(screen, particles, key_positions, keys_being_pressed)
        await asyncio.sleep(0)

    pygame.quit()

# This is the program entry point:
asyncio.run(main_loop())
