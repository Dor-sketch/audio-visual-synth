"""
This script generates a simple melody using the generate_note function and
plays it using the simpleaudio library. The melody is based on the notes of
the Israeli national anthem, "Hatikva". The script uses the notes_color module
to convert note names to MIDI numbers and the particles module to create
visual effects for each note played.
"""

import soundfile as sf
import pygame
import numpy as np
import simpleaudio as sa
from .particles import Particle, render_scene
from .notes_color import note_to_midi
from .hatikva import hatikva_notes
from .init import init_pygame


def validate_input(note, duration, volume, sample_rate, attack_time, decay_time, sustain_level, release_time):
    """
    Validate the input parameters for the generate_note function.

    Parameters:
        note (int or list): The MIDI note number or a list of MIDI note numbers.
        duration (float): The duration of the note in seconds.
        volume (float): The volume of the note (0 to 1).
        sample_rate (int): The sample rate of the audio.
        attack_time (float): The attack time of the note in seconds.
        decay_time (float): The decay time of the note in seconds.
        sustain_level (float): The sustain level of the note (0 to 1).
        release_time (float): The release time of the note in seconds.

    Raises:
        ValueError: If any of the input parameters are invalid.
    """
    if not 0 <= volume <= 1:
        raise ValueError("Volume must be between 0 and 1")
    if not 0 <= attack_time <= duration:
        raise ValueError("Attack time must be between 0 and the duration")
    if not 0 <= decay_time <= duration:
        raise ValueError("Decay time must be between 0 and the duration")
    if not 0 <= sustain_level <= 1:
        raise ValueError("Sustain level must be between 0 and 1")
    if not 0 <= release_time <= duration:
        raise ValueError("Release time must be between 0 and the duration")
    if isinstance(note, list):
        for n in note:
            if not isinstance(n, int):
                raise ValueError(
                    "Note must be an integer or a list of integers")
    elif not isinstance(note, int):
        raise ValueError("Note must be an integer or a list of integers")
    if not isinstance(duration, (int, float)):
        raise ValueError("Duration must be a number")

def generate_single_note(
    note=64,
    duration=1.0,
    volume=0.5,
    sample_rate=44100,
    attack_time=0.01,
    decay_time=0.01,
    sustain_level=0.7,
    release_time=0.01,
):
    if duration < 0.1:
        duration = 0.1
    # adajust parametrs based on duration
    if duration < attack_time + decay_time + release_time:
        attack_time = duration * 0.1
        decay_time = duration * 0.1
        release_time = duration * 0.1
    # Convert MIDI note number to frequency
    base_frequency = 440 * 2 ** ((note - 69) / 12)

    # Generate the time values
    t_values = np.linspace(0, duration, int(duration * sample_rate), False)

    # Generate the note with harmonics
    note_samples = np.sin(base_frequency * t_values * 2 * np.pi)
    for harmonic in range(2, 5):
        note_samples += 0.5 / harmonic * np.sin(harmonic * base_frequency * t_values * 2 * np.pi)

    # Generate the ADSR envelope
    total_samples = len(note_samples)
    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    release_samples = int(release_time * sample_rate)
    sustain_samples = total_samples - attack_samples - decay_samples - release_samples

    if sustain_samples < 0:
        raise ValueError("Invalid envelope times: attack + decay + release > duration")

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
def generate_note(note, *args, **kwargs):
    if isinstance(note, list):
        # Generate all notes in the chord and return them as a list
        return [
            generate_single_note(n, *args, **kwargs)
            for n in note
        ]
    else:
        return [generate_single_note(note, *args, **kwargs)]
def notes_to_midi(chords):
    """
    Convert a list of chords in note names to a list of chords in MIDI numbers.

    Parameters:
        chords (list): A list of chords in note names.

    Returns:
        list: A list of chords in MIDI numbers.
    """
    midi_chords = []
    for chord in chords:
        try:
            if isinstance(chord, str):
                chord = [chord]
            midi_chord = [note_to_midi[note] for note in chord]
            midi_chords.append(midi_chord)
        except KeyError as e:
            print(f"Error: Note {e} not found in note_to_midi dictionary")
            return []
    return midi_chords


hatikva_notes = notes_to_midi(hatikva_notes)
hatikva_durations = [0.5] * len(hatikva_notes)  # Each note is a quarter note


def handle_event(event):
    if event.type == pygame.QUIT:
        return False
    return True

def get_current_time():
    return pygame.time.get_ticks()

def is_note_ready_to_play(cur_note, next_note_time):
    current_time = get_current_time()
    return cur_note < len(hatikva_notes) and current_time >= next_note_time

def get_note_and_duration(cur_note):
    note = hatikva_notes[cur_note]
    duration = hatikva_durations[cur_note]
    return note, duration
import threading

def generate_and_play_note(note=64, duration=1.0):
    # Generate the notes
    notes = generate_note(note, duration=duration)

    # Play each note in a separate thread
    for note_samples in notes:
        threading.Thread(target=sa.play_buffer, args=(note_samples, 1, 2, 44100)).start()

    return notes[0] if notes else None

def append_particle(particles, note):
    if particles is not None:
        particles.append(Particle(0, 0, 0, note))

def update_all_samples(all_samples, note_samples):
    if all_samples is None:
        all_samples = note_samples
    else:
        all_samples.extend(note_samples)
    return all_samples

def update_note_and_time(cur_note, duration):
    cur_note += 1
    next_note_time = get_current_time() + int(duration * 1000)
    return cur_note, next_note_time

def play_note(cur_note, next_note_time, all_samples=None, particles=None):
    if is_note_ready_to_play(cur_note, next_note_time):
        note, duration = get_note_and_duration(cur_note)
        note_samples = generate_and_play_note(note, duration)
        append_particle(particles, note)
        all_samples = update_all_samples(all_samples, note_samples)
        cur_note, next_note_time = update_note_and_time(cur_note, duration)
    return cur_note, next_note_time, all_samples


def main():
    init_pygame()
    running = True
    cur_note = 0
    next_note_time = pygame.time.get_ticks()
    all_samples = []
    particles = []

    while running:
        for event in pygame.event.get():
            running = handle_event(event)
        cur_note, next_note_time, all_samples = play_note(
            cur_note, next_note_time, all_samples, particles)
        render_scene(particles)

    sf.write("output.wav", all_samples, 44100)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
