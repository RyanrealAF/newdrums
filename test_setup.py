import librosa
import mido
import numpy as np
import scipy

print("All dependencies are installed correctly!")

# Test librosa
try:
    print("librosa version:", librosa.__version__)
except Exception as e:
    print(f"librosa error: {e}")

# Test mido
try:
    print("mido version:", mido.__version__)
except Exception as e:
    print(f"mido error: {e}")

# Test numpy
try:
    print("numpy version:", np.__version__)
    arr = np.array([1, 2, 3])
    print("numpy test passed:", arr)
except Exception as e:
    print(f"numpy error: {e}")

# Test scipy
try:
    print("scipy version:", scipy.__version__)
    from scipy import signal
    print("scipy test passed")
except Exception as e:
    print(f"scipy error: {e}")