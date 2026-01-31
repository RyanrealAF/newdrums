# Free Audio-to-MIDI Conversion for Visual Sync

This project provides tools to convert audio tracks (like Suno-generated music) into MIDI files for driving audio-reactive visuals in software like OBS, VVVV, or Processing.

## The Free Stack

*   **Audio Analysis:** Python + `librosa`
*   **MIDI Creation:** `mido` library
*   **Visual Software:** OBS Studio, VVVV, Processing, Pure Data, Sonic Pi

---

## Quick Start

For detailed setup instructions, see [SETUP.md](SETUP.md).

### 1. Install Dependencies

Ensure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

### 2. Generate MIDI from Audio

Run the conversion script on your audio track:

```bash
python audio_to_midi.py your_track.wav --output output.mid --bpm 120 --dynamic
```

*   `input`: Path to your audio file.
*   `--output` or `-o`: Path to the resulting MIDI file (default: `output.mid`).
*   `--bpm` or `-b`: BPM of the track to help with grid alignment (default: 120).
*   `--note` or `-n`: MIDI note number to use (default: 36/Kick Drum).
*   `--velocity` or `-v`: Fixed velocity or max velocity for dynamic mode (default: 90).
*   `--dynamic`: Enable dynamic velocity scaling based on onset strength.

### 3. Visualize Audio and Onsets

Use the visualizer to analyze and visualize your audio track:

```bash
# Static waveform and onset visualization (saves to visualization.png)
python visualizer.py your_track.wav

# Real-time onset visualizer (requires pygame)
python visualizer.py your_track.wav --type realtime
```

*   `--type`: Visualization type (static or realtime). Static is default.
*   Static visualization: Generates a high-resolution PNG file with waveform and onset strength envelope.
*   Real-time visualization: Opens a pygame window showing amplitude bars and onset indicators.

---

## Alternative: Go Audio-Reactive (No MIDI Needed)

Audio-reactive visuals are often easier and more reliable than MIDI conversion.

### Setup (5 minutes):

1.  **OBS Studio** → Add audio source (Suno track).
2.  **Add Filter** → "Audio Monitor" (routes to virtual audio cable).
3.  **Install VB-Audio Cable** (free virtual audio device).
4.  **Add Browser Source** in OBS.
5.  **Use a free audio visualizer**:
    *   [butterchurn](https://butterchurnviz.com/) (Winamp visualizer, web version)
    *   Sonic Visualiser
    *   projectM (Milkdrop fork)

Point the browser source at the visualizer URL. It will react to audio frequencies automatically.

---

## Free Visual Software That Reads MIDI

If you prefer using MIDI to trigger specific visual events:

*   **R#**: Hypothetical visual programming language or framework designed for real-time audio-visual performance and interactive media. See [R#.md](R#.md) for more information.
*   **VVVV**: Node-based visual programming.
*   **Processing**: Code-based visuals (Java).
*   **Pure Data + GEM**: Audio/visual patching.
*   **Sonic Pi**: Live coding, can trigger visuals via OSC.

All can route their output to OBS via virtual camera or NDI.

---

## Fastest Free Solution

**Resolume Avenue** has a free demo (watermarked):
1.  Load Suno track.
2.  Set audio reactivity on layers.
3.  Capture to OBS via NDI plugin.

Or use **Shotcut** (free video editor) to sync visuals manually if performance isn't live.
