import pygame


# Define a mapping from MIDI note numbers to colors
# Define a mapping from MIDI note numbers to colors
note_to_color = {
    60: (0.1, 0.1, 0.9),  # C4 - Dark Blue
    61: (0.2, 0.2, 0.8),  # C#4/Db4 - Medium Blue
    62: (0.3, 0.3, 0.7),  # D4 - Light Blue
    63: (0.4, 0.4, 0.6),  # D#4/Eb4 - Lighter Blue
    64: (0.5, 0.5, 0.5),  # E4 - Gray
    65: (0.4, 0.4, 0.6),  # F4 - Lighter Blue
    66: (0.3, 0.3, 0.7),  # F#4/Gb4 - Light Blue
    67: (0.2, 0.2, 0.8),  # G4 - Medium Blue
    68: (0.1, 0.1, 0.9),  # G#4/Ab4 - Dark Blue
    69: (0.2, 0.2, 0.8),  # A4 - Medium Blue
    70: (0.3, 0.3, 0.7),  # A#4/Bb4 - Light Blue
    71: (0.4, 0.4, 0.6),  # B4 - Lighter Blue
    72: (0.5, 0.5, 0.5),  # C5 - Gray
    73: (0.4, 0.4, 0.6),  # C#5/Db5 - Lighter Blue
    74: (0.3, 0.3, 0.7),  # D5 - Light Blue
    75: (0.2, 0.2, 0.8),  # D#5/Eb5 - Medium Blue
    76: (0.1, 0.1, 0.9),  # E5 - Dark Blue
    77: (0.2, 0.2, 0.8),  # F5 - Medium Blue
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
