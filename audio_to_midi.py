import argparse
import librosa
import mido
import numpy as np

def audio_to_midi(input_file, output_file, bpm, note, velocity, dynamic):
    print(f"Loading {input_file}...")
    try:
        y, sr = librosa.load(input_file)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return
    
    print("Analyzing audio for onsets...")
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    
    # Create MIDI file
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    ticks_per_beat = 480
    mid.ticks_per_beat = ticks_per_beat
    
    # Set tempo
    microseconds_per_beat = mido.bpm2tempo(bpm)
    track.append(mido.MetaMessage('set_tempo', tempo=microseconds_per_beat, time=0))
    
    events = []
    
    max_strength = np.max(onset_env) if len(onset_env) > 0 else 1
    
    for i, t in enumerate(onset_times):
        current_velocity = velocity
        if dynamic:
            frame_idx = onset_frames[i]
            if frame_idx < len(onset_env):
                strength = onset_env[frame_idx]
                norm_strength = strength / max_strength if max_strength > 0 else 0
                current_velocity = int(norm_strength * 127)
                current_velocity = max(1, min(127, current_velocity))
        
        # Note On
        events.append({'time': t, 'type': 'note_on', 'velocity': current_velocity})
        # Note Off (short duration later)
        events.append({'time': t + 0.1, 'type': 'note_off', 'velocity': 0})
        
    events.sort(key=lambda x: x['time'])
    
    last_time = 0
    
    for event in events:
        delta_seconds = event['time'] - last_time
        # Convert seconds to ticks based on BPM
        delta_ticks = int(delta_seconds * (bpm * ticks_per_beat) / 60)
        delta_ticks = max(0, delta_ticks)
        
        track.append(mido.Message(event['type'], note=note, velocity=event['velocity'], time=delta_ticks))
        last_time = event['time']
        
    print(f"Saving MIDI to {output_file}...")
    mid.save(output_file)
    print(f"Done! Created {len(onset_times)} notes.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert audio to MIDI")
    parser.add_argument("input", help="Path to input audio file")
    parser.add_argument("--output", "-o", default="output.mid", help="Path to output MIDI file")
    parser.add_argument("--bpm", "-b", type=int, default=120, help="BPM of the track")
    parser.add_argument("--note", "-n", type=int, default=36, help="MIDI note number")
    parser.add_argument("--velocity", "-v", type=int, default=90, help="Velocity")
    parser.add_argument("--dynamic", action="store_true", help="Enable dynamic velocity")
    
    args = parser.parse_args()
    
    audio_to_midi(args.input, args.output, args.bpm, args.note, args.velocity, args.dynamic)