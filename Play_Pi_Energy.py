import numpy as np
import simpleaudio as sa
import matplotlib.pyplot as plt
from mpmath import mp

# Define energy to MIDI note mapping
midi_base = 60  # Middle C
energy_to_midi = {
    -5: midi_base - 12,  # Lower octave
    -4: midi_base - 9,
    -3: midi_base - 7,
    -2: midi_base - 5,
    -1: midi_base - 2,
    1: midi_base + 2,
    2: midi_base + 5,
    3: midi_base + 7,
    4: midi_base + 9,
    5: midi_base + 12  # Higher octave
}


# Function to map digits of Pi to energy values
def map_pi_to_energy(pi_digits):
    energy_mapping = {
        '0': -5, '1': -4, '2': -3, '3': -2, '4': -1,
        '5': 1, '6': 2, '7': 3, '8': 4, '9': 5
    }
    return [energy_mapping[d] for d in pi_digits]


# Function to generate and return Pi digits from start to start + n
def get_pi_digits(start, n):
    mp.dps = start + n + 2  # Set precision to include the required range
    pi_str = str(mp.pi)[2:]  # Remove "3."
    return pi_str[start:start + n]


# Function to play notes from energy values
def play_pi_as_sound(energy_values):
    sample_rate = 44100
    duration = 0.23  # seconds per note
    fade_time = round(duration/3,2)  # fade-in/out duration in seconds

    audio = np.array([])

    for value in energy_values:
        midi_note = energy_to_midi[value]
        frequency = 220.0 * (2 ** ((midi_note - 69) / 12.0))  # Convert MIDI to Hz
        t = np.linspace(0, duration, int(sample_rate * duration), False)

        # Generate sine wave
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)

        # Apply fade-in and fade-out to make the sound smoother
        fade_samples = int(fade_time * sample_rate)
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        wave[:fade_samples] *= fade_in
        wave[-fade_samples:] *= fade_out

        # Concatenate the processed wave
        audio = np.concatenate((audio, wave))

    # Normalize audio to prevent clipping
    audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)

    # Play the generated sound
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
    play_obj.wait_done()



# Function to visualize energy values sequentially
def scroll_pi_visualization(energy_values, digits, delay=0.3):
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 4))
    for i in range(len(energy_values)):
        ax.clear()
        ax.plot(energy_values[:i + 1], marker='o', label="Energy Values")
        ax.set_title(f"Scrolling Pi Digits: {digits[:i + 1]}")
        ax.set_xlabel("Index")
        ax.set_ylabel("Energy Value")
        ax.legend()
        ax.grid(True)
        plt.draw()
        plt.pause(delay)
    plt.ioff()
    plt.show()


# Input the starting index and the number of digits to play and visualize
start_index = int(input("Enter the starting index of Pi: "))
num_digits = int(input("Enter the number of digits of Pi to process: "))

# Get the specified range of Pi digits
pi_digits = get_pi_digits(start_index, num_digits)

# Map the digits to energy values
energy_values = map_pi_to_energy(pi_digits)

# Run visualization first, then play audio
#scroll_pi_visualization(energy_values, pi_digits)
play_pi_as_sound(energy_values)
