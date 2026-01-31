import argparse
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import sys

def static_viz(input_file):
    print(f"Generating static visualization for {input_file}...")
    try:
        y, sr = librosa.load(input_file)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    
    plt.figure(figsize=(14, 6))
    plt.subplot(2, 1, 1)
    librosa.display.waveshow(y, sr=sr, alpha=0.6)
    plt.title('Waveform')
    
    plt.subplot(2, 1, 2)
    plt.plot(librosa.times_like(onset_env, sr=sr), onset_env, label='Onset Strength')
    plt.legend(loc='upper right')
    plt.title('Onset Strength')
    
    output_file = "visualization.png"
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"Saved to {output_file}")

def realtime_viz(input_file):
    try:
        import pygame
    except ImportError:
        print("pygame is required for realtime visualization. Run: pip install pygame")
        return

    print(f"Starting realtime visualization for {input_file}...")
    
    y, sr = librosa.load(input_file)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    times = librosa.times_like(onset_env, sr=sr)
    
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Audio Visualizer")
    clock = pygame.time.Clock()
    
    pygame.mixer.music.load(input_file)
    pygame.mixer.music.play()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((20, 20, 20))
        
        current_time = pygame.mixer.music.get_pos() / 1000.0
        idx = np.searchsorted(times, current_time)
        
        if idx < len(onset_env):
            strength = onset_env[idx]
            radius = int(strength * 100)
            color_val = min(255, int(strength * 20))
            pygame.draw.circle(screen, (255, 100, 100), (width//2, height//2), radius)
            
        pygame.display.flip()
        clock.tick(60)
        
        if not pygame.mixer.music.get_busy():
            running = False

    pygame.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input audio file")
    parser.add_argument("--type", default="static", choices=["static", "realtime"], help="Visualization type")
    args = parser.parse_args()
    
    if args.type == "static":
        static_viz(args.input)
    else:
        realtime_viz(args.input)