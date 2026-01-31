import librosa
import mido
import numpy as np
import argparse
import sys
from mido import MidiFile, MidiTrack, Message, MetaMessage

def generate_midi(input_file, output_file, bpm, note=36, velocity=90, dynamic_velocity=False):
    # Load audio
    print(f"Loading {input_file}...")
    try:
        y, sr = librosa.load(input_file, sr=None)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        sys.exit(1)

    # Harmonic-Percussive Source Separation (HPSS)
    # This isolates percussive elements (drums) from melodic ones
    print("Separating percussive elements...")
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # Detect onset envelopes on percussive track for cleaner hits
    print("Detecting onsets...")
    onset_env = librosa.onset.onset_strength(y=y_percussive, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, backtrack=True)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    # Calculate velocities
    if dynamic_velocity and len(onset_frames) > 0:
        strengths = onset_env[onset_frames]
        max_strength = np.max(strengths)
        if max_strength > 0:
            # Scale to 1-127 range based on relative strength, maxing at requested velocity
            velocities = (strengths / max_strength * (velocity - 1) + 1).astype(int)
        else:
            velocities = np.full(len(onset_frames), velocity)
    else:
        velocities = np.full(len(onset_times), velocity)

    # Initialize MIDI
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    ticks_per_beat = 480
    tempo = mido.bpm2tempo(bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo))

    current_tick = 0
    duration_ticks = 10
    
    print(f"Processing {len(onset_times)} onsets...")

    for i, time in enumerate(onset_times):
        # Calculate absolute tick position
        target_tick = int(mido.second2tick(time, ticks_per_beat, tempo))
        
        # Note On
        delta_on = max(0, target_tick - current_tick)
        track.append(Message('note_on', note=note, velocity=int(velocities[i]), time=delta_on))
        current_tick += delta_on
        
        # Note Off (Fixed short duration for trigger-style visuals)
        track.append(Message('note_off', note=note, velocity=0, time=duration_ticks))
        current_tick += duration_ticks

    mid.save(output_file)
    print(f"Successfully created: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Convert audio to MIDI for visual sync.')
    parser.add_argument('input', help='Path to the input audio file (e.g., .wav, .mp3)')
    parser.add_argument('--output', '-o', default='output.mid', help='Path to the output MIDI file (default: output.mid)')
    parser.add_argument('--bpm', '-b', type=float, default=120.0, help='BPM of the track (default: 120)')
    parser.add_argument('--note', '-n', type=int, default=36, help='MIDI note number (default: 36/Kick Drum)')
    parser.add_argument('--velocity', '-v', type=int, default=90, help='Fixed velocity or max velocity (default: 90)')
    parser.add_argument('--dynamic', action='store_true', help='Use dynamic velocity based on onset strength')

    args = parser.parse_args()

    generate_midi(args.input, args.output, args.bpm, args.note, args.velocity, args.dynamic)

if __name__ == "__main__":
    main()
