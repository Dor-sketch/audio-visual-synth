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
from particles import Particle, render_scene
from notes_color import note_to_midi
from hatikva import hatikva_notes
from init import init_pygame


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


def generate_note(
    note,
    duration=0.1,
    volume=0.5,
    sample_rate=44100,
    attack_time=0.1,
    decay_time=0.1,
    sustain_level=0.5,
    release_time=0.1,
):
    """
    Generate a note with the given parameters.

    Parameters:
        note (int or list): The MIDI note number or a list of MIDI note numbers.
        duration (float): The duration of the note in seconds.
        volume (float): The volume of the note (0 to 1).
        sample_rate (int): The sample rate of the audio.
        attack_time (float): The attack time of the note in seconds.
        decay_time (float): The decay time of the note in seconds.
        sustain_level (float): The sustain level of the note (0 to 1).
        release_time (float): The release time of the note in seconds.

    Returns:
        numpy.ndarray: The audio samples of the note.
    """
    try:
        validate_input(note, duration, volume, sample_rate,
                       attack_time, decay_time, sustain_level, release_time)
    except ValueError as e:
        print(f"Error: {e}")
        return np.array([])

    if isinstance(note, list):
        return np.concatenate(
            [
                generate_note(
                    n,
                    duration=duration,
                    volume=volume,
                    sample_rate=sample_rate,
                    attack_time=attack_time,
                    decay_time=decay_time,
                    sustain_level=sustain_level,
                    release_time=release_time,
                )
                for n in note
            ]
        )

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


def play_note(cur_note, next_note_time, all_samples, particles):
    current_time = pygame.time.get_ticks()
    if cur_note < len(hatikva_notes) and current_time >= next_note_time:
        note = hatikva_notes[cur_note]
        duration = hatikva_durations[cur_note]
        note_samples = generate_note(note, duration=duration)
        sa.play_buffer(note_samples, 1, 2, 44100)
        particles.append(Particle(0, 0, 0, note))
        cur_note += 1
        next_note_time = current_time + int(duration * 1000)
        all_samples.extend(note_samples)
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
