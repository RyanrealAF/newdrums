import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pygame
import sys
import argparse

def plot_waveform_and_onsets(input_file):
    """Plot waveform with detected onsets using matplotlib (static visualization)."""
    print(f"Loading {input_file}...")
    try:
        y, sr = librosa.load(input_file, sr=None)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        sys.exit(1)

    # Harmonic-Percussive Source Separation
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # Detect onsets
    print("Detecting onsets...")
    onset_env = librosa.onset.onset_strength(y=y_percussive, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, backtrack=True)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    onset_samples = librosa.time_to_samples(onset_times, sr=sr)

    # Create time axis for waveform
    time_axis = np.arange(len(y)) / sr

    # Plot
    plt.figure(figsize=(15, 8))
    
    # Waveform
    plt.subplot(2, 1, 1)
    plt.plot(time_axis, y, label='Waveform')
    plt.vlines(onset_times, -np.max(np.abs(y)), np.max(np.abs(y)), color='r', label='Onsets')
    plt.title('Audio Waveform with Onset Detection')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Onset strength envelope
    plt.subplot(2, 1, 2)
    frame_times = librosa.frames_to_time(np.arange(len(onset_env)), sr=sr)
    plt.plot(frame_times, onset_env, label='Onset Strength')
    plt.vlines(onset_times, 0, np.max(onset_env), color='r', label='Onsets')
    plt.title('Onset Strength Envelope')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Strength')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('visualization.png', dpi=300, bbox_inches='tight')
    print("Static visualization saved as visualization.png")
    plt.show()

def real_time_onset_visualizer(input_file):
    """Real-time onset visualizer using pygame (requires audio playback)."""
    print(f"Loading {input_file}...")
    try:
        y, sr = librosa.load(input_file, sr=None)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        sys.exit(1)

    # Harmonic-Percussive Source Separation
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # Detect onsets
    print("Detecting onsets...")
    onset_env = librosa.onset.onset_strength(y=y_percussive, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, backtrack=True)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    # Initialize pygame
    pygame.init()
    width, height = 800, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Real-Time Onset Visualizer')
    clock = pygame.time.Clock()

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    # Visualization parameters
    bar_width = 4
    bar_spacing = 2
    num_bars = width // (bar_width + bar_spacing)
    max_amplitude = np.max(np.abs(y))

    # Time tracking
    current_time = 0
    onset_index = 0
    playback_rate = 1.0
    frame_rate = 60

    # Create amplitude data for visualization
    hop_length = len(y) // num_bars
    amplitudes = []
    for i in range(num_bars):
        start = i * hop_length
        end = (i + 1) * hop_length
        amplitudes.append(np.mean(np.abs(y[start:end])))

    amplitudes = np.array(amplitudes)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Clear screen
        screen.fill(BLACK)

        # Draw amplitude bars
        for i in range(num_bars):
            height_scaled = int((amplitudes[i] / max_amplitude) * height)
            x = i * (bar_width + bar_spacing)
            y_pos = height - height_scaled
            
            # Color based on amplitude
            color = (
                min(255, int(height_scaled / height * 255)),
                min(255, int((1 - height_scaled / height) * 255)),
                128
            )
            
            pygame.draw.rect(screen, color, (x, y_pos, bar_width, height_scaled))

        # Check for onset
        if onset_index < len(onset_times) and current_time >= onset_times[onset_index]:
            # Draw onset indicator
            pygame.draw.rect(screen, RED, (0, 0, width, height), 5)
            pygame.display.flip()
            pygame.time.wait(100)
            onset_index += 1

        # Update display
        pygame.display.flip()

        # Update time
        current_time += 1 / frame_rate

        # Limit frame rate
        clock.tick(frame_rate)

    pygame.quit()

def main():
    parser = argparse.ArgumentParser(description='Audio Visualizer for MIDI Conversion')
    parser.add_argument('input', help='Path to the input audio file (e.g., .wav, .mp3)')
    parser.add_argument('--type', '-t', choices=['static', 'realtime'], 
                       default='static', help='Visualization type (static or realtime)')

    args = parser.parse_args()

    if args.type == 'static':
        plot_waveform_and_onsets(args.input)
    elif args.type == 'realtime':
        real_time_onset_visualizer(args.input)

if __name__ == "__main__":
    main()