import sounddevice as sd
import numpy as np
import aubio
import math
import pygame

# Standards
width = 1020
height = 750

black = (0, 0, 0)
white = (255, 255, 255)
turquoise = (0, 200, 200)
light_blue = (100, 120, 185)
midnight_blue = (35, 35, 122)
ground_color = (10, 10, 92)
brown = (187, 109, 62)
dark_brown = (123, 56, 15)
indigo = (255, 220, 255)
pink = (255, 105, 180)

# Initialize
pygame.init()
pygame.display.set_caption('Pitch Sprint')
pygame.font.init()

# Make window
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
# Fonts
duenn_dick = pygame.font.SysFont('bahnenschrift.ttf', 50)

samplerate = 44100
win_s = 4096
hop_s = 512

pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("Hz")
pitch_o.set_silence(-40)
pitchy = pygame.image.load("img.png")
pitchy = pygame.transform.scale(pitchy, (150, 150))


def get_pitch():
    stream = sd.InputStream(channels=1, samplerate=samplerate, blocksize=hop_s)
    pitches = []
    with stream:
        print("🎤 Sing something...")
        for _ in range(50):
            data, _ = stream.read(hop_s)
            samples = np.frombuffer(data, dtype=np.float32)
            frequency = pitch_o(samples)[0]
            if frequency > 0:
                pitches.append(frequency)
    avg_pitch = np.median(pitches)
    print(f"🎯 Detected pitch: {avg_pitch:.2f} Hz")
    return avg_pitch


def freq_to_note_name(freq):
    if freq is None or isinstance(freq, str) or freq <= 0 or math.isnan(freq):
        return None  # Return None if the frequency is invalid or a string

    # Compute the MIDI note number
    midi_number = round(69 + 12 * math.log2(freq / 440.0))

    # Convert MIDI number to note
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_name = notes[(midi_number - 21) % 12]
    octave = (midi_number - 21) // 12
    return f"{note_name}{octave}"


def draw_UI():
    window.fill(midnight_blue)
    pygame.draw.rect(window, ground_color, (0, height - 100, width, 100))
    window.blit(pitchy, (300, 200))


def create_tone_scale(screen, singing_note, font):
    screen_height = screen.get_height()
    # Key sizes
    white_key_height = 70
    white_key_width = 60
    black_key_height = 35
    black_key_width = 35
    spacing = 8
    # Vertical offsets
    white_key_lift = 100
    black_key_lift = 60

    # Notes
    white_notes = ["C3", "D3", "E3", "F3", "G3", "A3", "B3", "C4"]
    black_notes_map = {
        "C#3": ("C3", "D3"),
        "D#3": ("D3", "E3"),
        "F#3": ("F3", "G3"),
        "G#3": ("G3", "A3"),
        "A#3": ("A3", "B3"),
    }

    margin_left = 20
    white_key_positions = {}

    # --- Draw white keys ---
    for i, note in enumerate(white_notes):
        y = screen_height - (i + 1) * (white_key_height + spacing) + spacing - white_key_lift
        x = margin_left
        color = (255, 255, 255)
        if note == singing_note:  # Highlight the singing note in pink
            color = (255, 46, 99)

        rect = pygame.Rect(x, y, white_key_width, white_key_height)
        pygame.draw.rect(screen, color, rect, border_radius=4)
        pygame.draw.rect(screen, (30, 30, 30), rect, 2)

        white_key_positions[note] = y  # Save for black key placement

        # Note label
        label = font.render(note, True, (20, 20, 20))
        screen.blit(label, (x + 8, y + white_key_height // 2 - 10))

    # --- Draw black keys ---
    for note, (lower, upper) in black_notes_map.items():
        if lower in white_key_positions and upper in white_key_positions:
            y_lower = white_key_positions[lower]
            y_upper = white_key_positions[upper]
            y = (y_lower + y_upper) // 2 - black_key_height // 2 - (black_key_lift - white_key_lift)

            # Adjust x-coordinate so black keys are placed between white keys
            x = margin_left + white_key_width - black_key_width // 2
            color = (0, 0, 0)
            if note == singing_note:  # Highlight the singing note in pink
                color = (255, 46, 99)

            rect = pygame.Rect(x, y, black_key_width, black_key_height)
            pygame.draw.rect(screen, color, rect, border_radius=3)


# Detect pitch once before entering main loop
pitch = get_pitch()
note = freq_to_note_name(pitch)
print(f"🎵 Note: {note}")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_UI()
    current_frequency = get_pitch()  # From your pitch detection
    print(current_frequency)
    current_note = freq_to_note_name(current_frequency)
    print(current_note)
    create_tone_scale(window, current_note, duenn_dick)

    pygame.display.flip()
    clock.tick(1)

pygame.quit()
