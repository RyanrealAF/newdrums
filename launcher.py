import sys
import os
import subprocess
import time

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
        # Construct command for audio_to_midi.py
        cmd_convert = [
            sys.executable, "audio_to_midi.py", 
            audio_path,
            "--output", midi_path,
            "--bpm", "120",
            "--dynamic"
        ]
        subprocess.check_call(cmd_convert)
        print("Conversion complete.")
        time.sleep(1.5)
        
        # Step 2: Run Visualizer
        print("\n[2/2] Launching Visualizer...")
        cmd_viz = [sys.executable, "rsharp.py", midi_path, "--bpm", "120", "--audio", audio_path]
        subprocess.check_call(cmd_viz)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()