import sys

def test_imports():
    print("Testing dependencies...")
    packages = ["librosa", "mido", "numpy", "scipy", "pygame", "matplotlib"]
    missing = []
    
    for p in packages:
        try:
            __import__(p)
            print(f"[OK] {p}")
        except ImportError:
            print(f"[FAIL] {p}")
            missing.append(p)
            
    if missing:
        print("\nMissing dependencies. Please run: pip install -r requirements.txt")
        sys.exit(1)
    else:
        print("\nAll dependencies installed correctly!")
        sys.exit(0)

if __name__ == "__main__":
    test_imports()