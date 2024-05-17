"""
WIP: This code is a work in progress. It is not yet complete and may not work as expected.
This script defines a simple music notes editor using Pygame. The editor allows the user to
click on buttons representing different notes to generate and play the corresponding notes.
The script uses the generate_note function from the music module to generate the notes and the
note_to_midi function to convert note names to MIDI numbers.
"""

import pygame
import numpy as np
from .music import generate_note, note_to_midi
# Your generate_note function here

# Initialize Pygame
pygame.init()

# Set the size and title of the window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Music Notes Editor")

# Define the notes and their corresponding MIDI numbers
notes = {
    'C': 60,
    'D': 62,
    'E': 64,
    'F': 65,
    'G': 67,
    'A': 69,
    'B': 71
}

# Create buttons for each note
buttons = {note: pygame.Rect(i * 100, 0, 90, 90) for i, note in enumerate(notes)}

# Loop until the user clicks the close button
done = False
clock = pygame.time.Clock()

while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()

            # Check if a note button was clicked
            for note, rect in buttons.items():
                if rect.collidepoint(pos):
                    # Generate the note and play it
                    audio = generate_note(notes[note])
                    sd.play(audio, blocking=True)

    # --- Drawing code
    screen.fill((255, 255, 255))
    for note, rect in buttons.items():
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        font = pygame.font.Font(None, 36)
        text = font.render(note, 1, (10, 10, 10))
        screen.blit(text, rect.move(30, 30))

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()