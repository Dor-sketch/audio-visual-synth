import cv2
import numpy as np
import pyautogui

STARTING_MIDI_NOTE = 64  # E4
STAFF_LINES = 5
SEMITONE = 1
RED = (0, 0, 255)
GREEN = (0, 255, 0)


def image_to_midi(image_path=None):
    """
    Converts an image of sheet music into MIDI note numbers by automatically detecting staff lines and their spacing.

    Args:
        image_path (str): Path to the sheet music image.

    Returns:
        list of int: MIDI note numbers, empty if fails.
    """
    # Load the image in grayscale
    # img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    screenshot = pyautogui.screenshot(region=(0, 0, 900, 600))
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if img is None:
        print("Error: Image could not be loaded. Please check the file path.")
        return []

    # Enhance contrast
    img = cv2.equalizeHist(img)

    # Binarization of the image using Otsu's method
    _, img_bin = cv2.threshold(
        img, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    horizontal_lines = []
    # Detect horizontal lines
    lines = cv2.HoughLinesP(img_bin, 1, np.pi / 180, 100,
                            minLineLength=100, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y1 - y2) < 5:
                horizontal_lines.append(line)

    # Morphological operations to emphasize lines
    kernel = np.ones((3, 3), np.uint8)
    img_morph = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(
        img_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    midi_notes = []
    num_staff_lines = STAFF_LINES
    midi_note = STARTING_MIDI_NOTE

    # Sort the lines from top to bottom
    horizontal_lines = sorted(horizontal_lines, key=lambda line: line[0][1])

    # Collect notes in spaces
    notes_in_spaces = [cv2.boundingRect(
        cmt) for cmt in contours if cv2.boundingRect(cmt)[3] < 10]

    # remove first note in each staff (that is the clef)

    for i in range(len(horizontal_lines)):
        x1, y1, x2, y2 = horizontal_lines[i][0]
        cv2.line(img_color, (x1, y1), (x2, y2), GREEN, 2)

        # Assign MIDI note to this line
        midi_notes.append(midi_note)
        midi_note -= SEMITONE  # Decrease the note by one semitone

        # Reset the MIDI note and the staff line count after every 5 lines
        if (i + 1) % STAFF_LINES == 0:
            midi_note = STARTING_MIDI_NOTE

        cv2.rectangle(img_color, (x1, y1), (x2, y2), GREEN, 2)
        # add text for debugging
        cv2.putText(img_color, str(
            midi_notes[-1]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, RED, 2)

    # Now, for each note in the space between lines, find the closest line and assign a MIDI note based on its relative position
    # Now, for each note in the space between lines, find the closest line and assign a MIDI note based on its relative position
    for note in notes_in_spaces:
        # Find the closest line
        closest_line_index = min(range(len(horizontal_lines)), key=lambda i: min(
            abs(y - note[1]) for y in horizontal_lines[i][0]))
        # Determine the relative location of the note to the closest line
        if note[1] >= horizontal_lines[closest_line_index][0][1]:  # If the note is below the line
            midi_note_for_space = midi_notes[closest_line_index] - SEMITONE
        else:  # If the note is above the line
            midi_note_for_space = midi_notes[closest_line_index] + SEMITONE
        # Add the MIDI note for the space to the list of MIDI notes
        midi_notes.append(midi_note_for_space)
        # add text to the image for debugging
        cv2.putText(img_color, str(midi_note_for_space),
                    (note[0], note[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, RED, 2)
    cv2.imshow('Detected Notes', img_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return midi_notes


if __name__ == "__main__":
    # image_path = "hatikva-sheet-music-image.jpg"
    midi_notes = image_to_midi()
    print(midi_notes)
