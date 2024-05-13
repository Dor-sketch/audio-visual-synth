"""
This file contains the notes for the melody and harmony of the Israeli national anthem, Hatikva.
The notes are represented as tuples of the melody note and the harmony note.
"""

hatikva_melody = [
    "D4",
    "E4",
    "F4",
    "G4",
    "A4",
       "A4",
       "A4",
    "A4",
    "Bb4",
    "A4",
    "Bb4",
    "D5",
    "A4",
    "A4",
    "A4",
    "A4",
    "G4",
        "G4",

    "G4",
    "G4",
    "F4",
    "F4",
    "F4",
    "F4",
    "E4",
    "D4",
    "E4",
    "F4",
    "D4",
    "D4",

    "D4",
    "A3"]*2 + [
    "D4",
    "D4",
    "D5",
    "D5",
    "D5",
    "D5",
    "D5",
    "D5",
    "C5",
    "D5",
    "C5",
    "Bb4",
    "A4",
    "A4",
    "A4",
    "A4"]*2 + [
    "C5",
    "C5",
    "C5",
    "C5",
    "F4",
    "F4",
    "F4",
    "F4",
    "G4",
    "A4",
    "Bb4",
    "C5",
    "A4",
    "A4",
    "G4",
    "F4",
    "G4",
    "G4",
    "G4",
    "G4",
    "F4",
    "F4",
    "F4",
    "F4",
    "E4",
    "D4",
    "E4",
    "F4",
    "D4"]
hatikva_harmony = [
    "D3",  # Root note of D minor chord
    "C3",  # Seventh of D minor chord
    "A2",  # Fifth of D minor chord
    "Bb2", # Root note of Bb major chord
    "C3",  # Second of Bb major chord
    "D3",  # Root note of D minor chord
    "C3",  # Seventh of D minor chord
    "E3",  # Third of C major chord (passing tone)
    "D3",  # Root note of D minor chord
    "C3",  # Seventh of D minor chord
    "Bb2", # Root note of Bb major chord
    "A2",  # Fifth of D minor chord
    "G2",  # Fourth of D minor chord (passing tone)
    "A2",  # Fifth of D minor chord
    "G2",  # Fourth of D minor chord
    "F2",  # Third of D minor chord
    "E2",  # Second of D minor chord (passing tone)
    "D2",  # Root note of D minor chord
    "C2",  # Seventh of D minor chord
    "Bb1", # Root note of Bb major chord
    "A2",  # Fifth of D minor chord
    "G2",  # Fourth of D minor chord
    "A2",  # Fifth of D minor chord
    "G2",  # Fourth of D minor chord
    "F2",  # Third of D minor chord
    "E2",  # Second of D minor chord (passing tone)
    "D2",  # Root note of D minor chord
    "C2",  # Seventh of D minor chord
    "Bb1", # Root note of Bb major chord
    "A2",  # Fifth of D minor chord
    "G2",  # Fourth of D minor chord
    "F2"   # Third of D minor chord
]*2 + [
    "E2",  # Second of D minor chord
    "D2",  # Root note of D minor chord
    "C2",  # Seventh of D minor chord
    "Bb1", # Root note of Bb major chord
    "A2",  # Fifth of D minor chord
    "G2",  # Fourth of D minor chord
    "F2",  # Third of D minor chord
    "E2",  # Second of D minor chord
    "D2",  # Root note of D minor chord
    "C2",  # Seventh of D minor chord
    "Bb1", # Root note of Bb major chord
    "A2",  # Fifth of D minor chord
    "G2",  # Fourth of D minor chord
    "F2",  # Third of D minor chord
    "E2",  # Second of D minor chord
    "D2"   # Root note of D minor chord
]*2 + [
    "C2",  # Seventh of D minor chord
    "Bb1", # Root note of Bb major chord
    "A2",  # Fifth of D minor chord
    "G2",  # Fourth of D minor chord
    "F2",  # Third of D minor chord
    "E2",  # Second of D minor chord
    "D2",  # Root note of D minor chord
    "C2",  # Seventh of D minor chord
    "Bb1", # Root note of Bb major chord
    "A2",  # Fifth of D minor chord
    "G2",  # Fourth of D minor chord
    "F2",  # Third of D minor chord
    "E2",  # Second of D minor chord
    "D2",  # Root note of D minor chord
    "C2",  # Seventh of D minor chord
    "Bb1", # Root note of Bb major chord
    "A2",  # Fifth of D minor chord
    "G2",  # Fourth of D minor chord
    "F2",  # Third of D minor chord
    "E2",  # Second of D minor chord
    "D2",  # Root note of D minor chord
    "C2",  # Seventh of D minor chord
    "Bb1", # Root note of Bb major chord
    "A2",  # Fifth of D minor chord
    "G2",  # Fourth of D minor chord
    "F2",  # Third of D minor chord
    "E2",  # Second of D minor chord
    "D2"   # Root note of D minor chord
]

hatikva_notes = list(zip(hatikva_melody, hatikva_harmony))
hatikva_notes = hatikva_melody