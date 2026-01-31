import sys
import os
import time

try:
    from audio_to_midi import audio_to_midi
    from rsharp import RSharp, DrumHitEffect, ParticleEmitterEffect
    import pygame
except ImportError as e:
    print(f"Error: Missing dependency {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

def main():
    # Check if a file was dropped or passed as argument
    if len(sys.argv) < 2:
        print("R# Visualizer Launcher")
        print("----------------------")
        print("Usage: Drag and drop an audio file (WAV/MP3) onto play.bat")
        print("       or run: python launcher.py <audio_file>")
        return

    audio_path = sys.argv[1]
    
    if not os.path.exists(audio_path):
        print(f"Error: File not found: {audio_path}")
        return

    # Get directory and filename
    directory = os.path.dirname(audio_path)
    filename = os.path.basename(audio_path)
    name_without_ext = os.path.splitext(filename)[0]
    
    # Define output MIDI path (same folder as audio)
    midi_path = os.path.join(directory, f"{name_without_ext}.mid")
    
    print(f"--- Processing: {filename} ---")
    
    # Step 1: Convert Audio to MIDI
    print("\n[1/2] Converting Audio to MIDI...")
    try:
        # Direct call to conversion function
        # audio_to_midi(input_file, output_file, bpm, note, velocity, dynamic)
        audio_to_midi(audio_path, midi_path, 120, 36, 90, True)
        print("Conversion complete.")
        time.sleep(1.5)
        
        # Step 2: Run Visualizer
        print("\n[2/2] Launching Visualizer...")
        
        # Initialize Visualizer
        rsharp = RSharp(midi_path, audio_file=audio_path, bpm=120)
        
        # Add effects
        drum_hits = DrumHitEffect(rsharp.screen_width, rsharp.screen_height)
        particle_emitter = ParticleEmitterEffect(rsharp.screen_width, rsharp.screen_height)
        
        rsharp.add_visual_effect(drum_hits)
        rsharp.add_visual_effect(particle_emitter)
        
        print("Starting R# visualizer...")
        print("Press ESC or close the window to exit")
        rsharp.run()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        # Keep console open briefly to show error
        time.sleep(5)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()