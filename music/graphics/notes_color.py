"""
This file contains mappings from note names to MIDI note numbers,
MIDI note numbers to colors, and keys to MIDI note numbers.

The `note_to_midi` dictionary maps note names to their corresponding MIDI note numbers.
For example, the note "C4" is mapped to the MIDI note number 60.

The `note_to_color` dictionary maps MIDI note numbers to RGB colors. For example,
the MIDI note number 60 (C4) is mapped to the color (0.0, 0.0, 0.5) which is a dark blue color.

The `key_to_note` dictionary maps Pygame key constants to MIDI note numbers.
For example, the key `pygame.K_a` is mapped to the MIDI note number 60 (C4).
"""


import pygame

note_to_midi = {
    "C0": 12,
    "C#0": 13,
    "Db0": 13,
    "D0": 14,
    "D#0": 15,
    "Eb0": 15,
    "E0": 16,
    "F0": 17,
    "F#0": 18,
    "Gb0": 18,
    "G0": 19,
    "G#0": 20,
    "Ab0": 20,
    "A0": 21,
    "A#0": 22,
    "Bb0": 22,
    "B0": 23,
    "C1": 24,
    "C#1": 25,
    "Db1": 25,
    "D1": 26,
    "D#1": 27,
    "Eb1": 27,
    "E1": 28,
    "F1": 29,
    "F#1": 30,
    "Gb1": 30,
    "G1": 31,
    "G#1": 32,
    "Ab1": 32,
    "A1": 33,
    "A#1": 34,
    "Bb1": 34,
    "B1": 35,
    "C2": 36,
    "C#2": 37,
    "Db2": 37,
    "D2": 38,
    "D#2": 39,
    "Eb2": 39,
    "E2": 40,
    "F2": 41,
    "F#2": 42,
    "Gb2": 42,
    "G2": 43,
    "G#2": 44,
    "Ab2": 44,
    "A2": 45,
    "A#2": 46,
    "Bb2": 46,
    "B2": 47,
    "C3": 48,
    "C#3": 49,
    "Db3": 49,
    "D3": 50,
    "D#3": 51,
    "Eb3": 51,
    "E3": 52,
    "F3": 53,
    "F#3": 54,
    "Gb3": 54,
    "G3": 55,
    "G#3": 56,
    "Ab3": 56,
    "A3": 57,
    "A#3": 58,
    "Bb3": 58,
    "B3": 59,
    "C4": 60,
    "C#4": 61,
    "Db4": 61,
    "D4": 62,
    "D#4": 63,
    "Eb4": 63,
    "E4": 64,
    "F4": 65,
    "F#4": 66,
    "Gb4": 66,
    "G4": 67,
    "G#4": 68,
    "Ab4": 68,
    "A4": 69,
    "A#4": 70,
    "Bb4": 70,
    "B4": 71,
    "C5": 72,
    "C#5": 73,
    "Db5": 73,
    "D5": 74,
    "D#5": 75,
    "Eb5": 75,
    "E5": 76,
    "F5": 77,
    "F#5": 78,
    "Gb5": 78,
    "G5": 79,
    "G#5": 80,
    "Ab5": 80,
    "A5": 81,
    "A#5": 82,
    "Bb5": 82,
    "B5": 83,
    "C6": 84,
    "C#6": 85,
    "Db6": 85,
    "D6": 86,
    "D#6": 87,
    "Eb6": 87,
    "E6": 88,
    "F6": 89,
    "F#6": 90,
    "Gb6": 90,
    "G6": 91,
    "G#6": 92,
    "Ab6": 92,
    "A6": 93,
    "A#6": 94,
    "Bb6": 94,
    "B6": 95,
    "C7": 96,
    "C#7": 97,
    "Db7": 97,
    "D7": 98,
    "D#7": 99,
    "Eb7": 99,
    "E7": 100,
    "F7": 101,
    "F#7": 102,
    "Gb7": 102,
    "G7": 103,
    "G#7": 104,
    "Ab7": 104,
    "A7": 105,
    "A#7": 106,
    "Bb7": 106,
    "B7": 107,
    "C8": 108,
    "C#8": 109,
    "Db8": 109,
    "D8": 110,
    "D#8": 111,
    "Eb8": 111,
    "E8": 112,
    "F8": 113,
    "F#8": 114,
    "Gb8": 114,
    "G8": 115,
    "G#8": 116,
    "Ab8": 116,
    "A8": 117,
    "A#8": 118,
    "Bb8": 118,
    "B8": 119,
    "C9": 120,
    "C#9": 121,
    "Db9": 121,
    "D9": 122,
    "D#9": 123,
    "Eb9": 123,
    "E9": 124,
    "F9": 125,
    "F#9": 126,
    "Gb9": 126,
    "G9": 127,
}

# Define a mapping from MIDI note numbers to colors
# Define a mapping from MIDI note numbers to colors
note_to_color = {
    60: (0.0, 0.0, 0.5),  # C4 - Dark Blue
    61: (0.0, 0.1, 0.6),  # C#4/Db4 - Darker Blue
    62: (0.0, 0.2, 0.7),  # D4 - Dark Blue
    63: (0.0, 0.3, 0.8),  # D#4/Eb4 - Dark Blue
    64: (0.0, 0.4, 0.9),  # E4 - Dark Blue
    65: (0.1, 0.5, 0.8),  # F4 - Dark Blue
    66: (0.2, 0.6, 0.7),  # F#4/Gb4 - Dark Blue
    67: (1, 1, 1),  # G4 - Darker Blue
    68: (0.4, 0.8, 0.5),  # G#4/Ab4 - Dark Blue
    69: (0.5, 0.1, 0.6),  # A4 - Darker Blue
    70: (0.6, 0.2, 0.7),  # A#4/Bb4 - Dark Blue
    71: (0.7, 0.7, 0.8),  # B4 - Dark Blue
    72: (1, 1, 1),  # C5 - Dark Blue
    73: (0.1, 0.5, 0.8),  # C#5/Db5 - Dark Blue
    74: (0.8, 0.4, 0.7),  # D5 - Dark Blue
    75: (0.7, 0.3, 0.6),  # D#5/Eb5 - Darker Blue
    76: (0.6, 0.2, 0.5),  # E5 - Dark Blue
    77: (0.5, 0.1, 0.6),  # F5 - Darker Blue
}


# Define a mapping from keys to MIDI note numbers
key_to_note = {
    pygame.K_a: 60,  # C4
    pygame.K_w: 61,  # C#4/Db4
    pygame.K_s: 62,  # D4
    pygame.K_e: 63,  # D#4/Eb4
    pygame.K_d: 64,  # E4
    pygame.K_f: 65,  # F4
    pygame.K_t: 66,  # F#4/Gb4
    pygame.K_g: 67,  # G4
    pygame.K_y: 68,  # G#4/Ab4
    pygame.K_h: 69,  # A4
    pygame.K_u: 70,  # A#4/Bb4
    pygame.K_j: 71,  # B4
    pygame.K_k: 72,  # C5
    pygame.K_o: 73,  # C#5/Db5
    pygame.K_l: 74,  # D5
    pygame.K_p: 75,  # D#5/Eb5
    pygame.K_SEMICOLON: 76,  # E5
    pygame.K_QUOTE: 77,  # F5
}
