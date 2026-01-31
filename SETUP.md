# Setup Guide

This guide provides detailed instructions for setting up and using the audio-to-MIDI conversion tool.

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## Installation

### 1. Install Dependencies

Run the following command to install all required dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- `librosa`: Audio analysis library
- `mido`: MIDI file handling library
- `numpy`: Numerical computing library
- `scipy`: Scientific computing library

### 2. Verify Installation

To verify that all dependencies are installed correctly, run the test script:

```bash
python test_setup.py
```

## Usage

### Converting Audio to MIDI

To convert an audio file to MIDI, use the following command:

```bash
python audio_to_midi.py <input_audio_file> --output <output_midi_file> --bpm <bpm> --dynamic
```

### Example

```bash
python audio_to_midi.py "track.wav" --output "output.mid" --bpm 120 --dynamic
```

### Parameters

- `input`: Path to the input audio file (required)
- `--output` or `-o`: Path to the resulting MIDI file (default: `output.mid`)
- `--bpm` or `-b`: BPM of the track (default: 120)
- `--note` or `-n`: MIDI note number to use (default: 36/Kick Drum)
- `--velocity` or `-v`: Fixed velocity or max velocity for dynamic mode (default: 90)
- `--dynamic`: Enable dynamic velocity scaling based on onset strength

## Testing the Setup

### 1. Check Python Version

```bash
python --version
```

### 2. Verify Dependencies are Installed

```bash
pip list | findstr /i "librosa mido numpy scipy"
```

### 3. Run the Test Script

```bash
python test_setup.py
```

### 4. Test with an Audio File

```bash
python audio_to_midi.py "track.wav" --output "test_output.mid" --bpm 120 --dynamic
```

### 5. Verify the Output MIDI File

```bash
python -c "import mido; mid = mido.MidiFile('test_output.mid'); print('MIDI file has', len(mid.tracks), 'tracks'); print('Total messages:', sum(len(track) for track in mid.tracks))"
```

## Troubleshooting

### Common Issues

1. **Dependencies not installed**: Make sure you ran `pip install -r requirements.txt`
2. **Python version too old**: Ensure you're using Python 3.6 or higher
3. **Audio file not found**: Check the path to the audio file is correct
4. **MIDI file not created**: Check the output path and permissions

### Error Messages

- **ModuleNotFoundError**: This indicates a dependency is not installed. Run `pip install -r requirements.txt`
- **FileNotFoundError**: The specified audio file could not be found. Check the path
- **RuntimeError**: There was an error processing the audio file. Try a different file format

## Advanced Setup

### Virtual Environment (Recommended)

For better dependency management, create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

### Updating Dependencies

To update dependencies to the latest versions:

```bash
pip install --upgrade -r requirements.txt
```

## Performance Tips

- Use WAV files for best performance
- Avoid very large audio files (more than 10 minutes)
- Reduce the audio file size before conversion if needed

## Additional Resources

- [librosa Documentation](https://librosa.org/doc/latest/index.html)
- [mido Documentation](https://mido.readthedocs.io/en/latest/)
- [numpy Documentation](https://numpy.org/doc/)
- [scipy Documentation](https://docs.scipy.org/doc/)