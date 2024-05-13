import cv2
import numpy as np
import pyautogui

STARTING_MIDI_NOTE = 64  # E4
STAFF_LINES = 5
SEMITONE = 1
RED = (0, 0, 255)
GREEN = (0, 255, 0)


def load_image(image_path=None):
    screenshot = pyautogui.screenshot(region=(0, 0, 900, 600))
    if screenshot is None:
        print("Error: Screenshot could not be captured.")
        return None, None
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if img is None:
        print("Error: Image could not be loaded. Please check the file path.")
        return None, None
    return img, img_color


def enhance_contrast(img):
    return cv2.equalizeHist(img)


def binarize_image(img):
    _, img_bin = cv2.threshold(
        img, 0, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return img_bin


def detect_horizontal_lines(img_bin):
    horizontal_lines = []
    lines = cv2.HoughLinesP(img_bin, 1, np.pi / 180, 100,
                            minLineLength=100, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if abs(y1 - y2) < 5:
                horizontal_lines.append(line)
    return horizontal_lines


def morphological_operations(img_bin):
    kernel = np.ones((3, 3), np.uint8)
    img_morph = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(
        img_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def collect_notes_in_spaces(contours):
    return [cv2.boundingRect(cmt) for cmt in contours if cv2.boundingRect(cmt)[3] < 10]


def assign_midi_notes(horizontal_lines, img_color):
    midi_notes = []
    midi_note = STARTING_MIDI_NOTE
    for i in range(len(horizontal_lines)):
        x1, y1, x2, y2 = horizontal_lines[i][0]
        cv2.line(img_color, (x1, y1), (x2, y2), GREEN, 2)
        midi_notes.append(midi_note)
        midi_note -= SEMITONE
        if (i + 1) % STAFF_LINES == 0:
            midi_note = STARTING_MIDI_NOTE
        cv2.rectangle(img_color, (x1, y1), (x2, y2), GREEN, 2)
        cv2.putText(img_color, str(
            midi_notes[-1]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, RED, 2)
    return midi_notes


def assign_midi_notes_for_spaces(notes_in_spaces, horizontal_lines, midi_notes, img_color):
    for note in notes_in_spaces:
        closest_line_index = min(range(len(horizontal_lines)), key=lambda i: min(
            abs(y - note[1]) for y in horizontal_lines[i][0]))
        if note[1] >= horizontal_lines[closest_line_index][0][1]:
            midi_note_for_space = midi_notes[closest_line_index] - SEMITONE
        else:
            midi_note_for_space = midi_notes[closest_line_index] + SEMITONE
        midi_notes.append(midi_note_for_space)
        cv2.putText(img_color, str(midi_note_for_space),
                    (note[0], note[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, RED, 2)
    return midi_notes


def image_to_midi(image_path=None):
    img, img_color = load_image(image_path)
    if img is None:
        return []
    img = enhance_contrast(img)
    img_bin = binarize_image(img)
    horizontal_lines = detect_horizontal_lines(img_bin)
    contours = morphological_operations(img_bin)
    notes_in_spaces = collect_notes_in_spaces(contours)
    midi_notes = assign_midi_notes(horizontal_lines, img_color)
    midi_notes = assign_midi_notes_for_spaces(
        notes_in_spaces, horizontal_lines, midi_notes, img_color)
    cv2.imshow('Detected Notes', img_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return midi_notes


if __name__ == "__main__":
    # image_path = "hatikva-sheet-music-image.jpg"
    midi_notes = image_to_midi('hatikva-sheet-music-image.jpg')
    print(midi_notes)
