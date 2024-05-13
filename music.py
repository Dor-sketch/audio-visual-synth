import pygame
import numpy as np
import simpleaudio as sa
from OpenGL.GL import *
from OpenGL.GLUT import *
from pygame.locals import *
from OpenGL.GLU import *
from particles import Particle
from notes_color import key_to_note, note_to_color

# Define a mapping from MIDI note numbers to colors
note_to_color1 = {
    60: (1, 0, 0),  # C4 - Red
    62: (0, 1, 0),  # D4 - Green
    64: (0, 0, 1),  # E4 - Blue
    65: (1, 1, 0),  # F4 - Yellow
    67: (1, 0, 1),  # G4 - Magenta
    68: (0, 1, 1),  # A4 - Cyan
    71: (1, 1, 1),  # B4 - White
    72: (0.5, 0.5, 0.5),  # C5 - Gray
}

# Initialize a variable to store the current note
current_note = None


particles = []


def generate_note(
    note,
    duration=10,
    volume=0.5,
    sample_rate=44100,
    attack_time=0.1,
    decay_time=0.1,
    sustain_level=0.5,
    release_time=0.1,
):
    # Convert MIDI note number to frequency
    frequency = 440 * 2 ** ((note - 69) / 12)

    # Generate the time values
    t_values = np.linspace(0, duration, int(duration * sample_rate), False)

    # Generate the note
    note_samples = np.sin(frequency * t_values * 2 * np.pi)

    # Generate the ADSR envelope
    total_samples = len(note_samples)
    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    release_samples = int(release_time * sample_rate)
    sustain_samples = total_samples - attack_samples - decay_samples - release_samples

    envelope = np.concatenate(
        [
            np.linspace(0, 1, attack_samples),  # Attack
            np.linspace(1, sustain_level, decay_samples),  # Decay
            np.full(sustain_samples, sustain_level),  # Sustain
            np.linspace(sustain_level, 0, release_samples),  # Release
        ]
    )

    # Apply the envelope to the note
    note_samples *= envelope

    # Convert to 16-bit PCM audio
    audio = note_samples * (2**15 - 1) * volume
    return audio.astype(np.int16)


def notes_to_midi(notes):
    # Mapping of note names to MIDI numbers
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

    # Convert note names to MIDI numbers
    midi_notes = [note_to_midi[note] for note in notes]

    return midi_notes


hatikva_notes = [
    "D4",
    "E4",
    "F4",
    "G4",
    "A4",
    "D4",
    "E4",
    "A4",
    "Bb4",
    "A4",
    "Bb4",
    "D5",
    "A4",
    "G4",
    "F4",
    "D4",
    "G4",
    "C4",
    "G4",
    "G4",
    "F4",
    "Bb3",
    "E4",
    "A3",
    "E4",
    "D4",
    "E4",
    "F4",
    "D4",
    "A3",
    "D4",
    "E4",
    "D4",
    "E4",
    "F4",
    "G4",
    "A4",
    "D4",
    "E4",
    "A4",
    "Bb4",
    "A4",
    "Bb4",
    "D5",
    "A4",
    "G4",
    "F4",
    "E4",
    "G4",
    "C4",
    "G4",
    "G4",
    "F4",
    "C4",
    "E4",
    "C4",
    "E4",
    "D4",
    "E4",
    "F4",
    "D4",
    "D4",
    "D4",
    "E4",
    "D4",
    "D5",
    "D5",
    "D5",
    "C5",
    "D5",
    "C5",
    "Bb4",
    "A4",
    "D4",
    "E4",
    "F4",
    "D4",
    "D4",
    "D5",
    "D5",
    "D5",
    "C5",
    "D5",
    "C5",
    "Bb4",
    "A4",
    "G4",
    "F4",
    "E4",
    "D5",
    "C5",
    "D5",
] * 2


hatikva_notes = notes_to_midi(hatikva_notes)
hatikva_durations = [0.5] * len(hatikva_notes)  # Each note is a quarter note


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    # set to white backround
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    running = True

    cur_note = 0
    # The time when the next note should be played
    next_note_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        if cur_note < len(hatikva_notes) and current_time >= next_note_time:
            note = hatikva_notes[cur_note]
            duration = hatikva_durations[cur_note]
            note_samples = generate_note(note, duration=duration)
            sa.play_buffer(note_samples, 1, 2, 44100)
            particles.append(Particle(0, 0, 0, note))
            cur_note += 1
            next_note_time = current_time + int(
                duration * 1000
            )  # Schedule the next note

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Update and draw all particles
        [p.move() for p in particles]
        [p.draw() for p in particles]

        pygame.display.flip()
        # Wait a short amount of time to limit the frame rate
        pygame.time.wait(10)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
