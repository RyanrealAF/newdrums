import argparse
import mido
import pygame
import numpy as np
import time
import sys

class RSharp:
    def __init__(self, midi_file, audio_file=None, bpm=120):
        self.midi_file = midi_file
        self.audio_file = audio_file
        self.bpm = bpm
        self.events = []
        self.event_index = 0
        self.current_time = 0
        self.running = False
        self.visual_effects = []
        
        # Initialize pygame
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("R# - MIDI Visualizer")
        
        # Load MIDI file
        self.load_midi_file()
        
        # Setup clock
        self.clock = pygame.time.Clock()
        
    def load_midi_file(self):
        """Load and parse MIDI file events"""
        try:
            mid = mido.MidiFile(self.midi_file)
            self.ticks_per_beat = mid.ticks_per_beat
            
            # Extract all note on/off events with timing
            time_in_ticks = 0
            for track in mid.tracks:
                for msg in track:
                    time_in_ticks += msg.time
                    if msg.type in ['note_on', 'note_off']:
                        # Convert ticks to seconds
                        time_in_seconds = (time_in_ticks / self.ticks_per_beat) * (60 / self.bpm)
                        self.events.append({
                            'time': time_in_seconds,
                            'type': msg.type,
                            'note': msg.note,
                            'velocity': msg.velocity
                        })
            
            # Sort events by time
            self.events.sort(key=lambda x: x['time'])
            print(f"Loaded MIDI file with {len(self.events)} events")
            
        except Exception as e:
            print(f"Error loading MIDI file: {e}")
            sys.exit(1)
            
    def add_visual_effect(self, effect):
        """Add a visual effect to the scene"""
        self.visual_effects.append(effect)

    def reset_visualizer(self):
        """Reset the visualizer state"""
        self.event_index = 0
        self.current_time = 0
        if self.audio_file:
            try:
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Error restarting audio: {e}")
        
        for effect in self.visual_effects:
            effect.reset()
        
    def process_events(self):
        """Process MIDI events based on current time"""
        # Find all events that should be triggered now
        triggered_events = []
        
        while self.event_index < len(self.events):
            event = self.events[self.event_index]
            if event['time'] <= self.current_time:
                triggered_events.append(event)
                self.event_index += 1
            else:
                break
                
        # Trigger visual effects for each event
        for event in triggered_events:
            for effect in self.visual_effects:
                effect.trigger(event)
                
    def update(self):
        """Update all visual effects"""
        for effect in self.visual_effects:
            effect.update()
            
    def draw(self):
        """Draw all visual effects (without flipping display)"""
        # Clear screen
        self.screen.fill((20, 20, 20))
        
        # Render effects
        for effect in self.visual_effects:
            effect.render(self.screen)
        
    def run(self):
        """Main loop"""
        self.running = True
        self.paused = False
        
        if self.audio_file:
            try:
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Error playing audio: {e}")
                
        start_time = time.time()
        
        # Pause tracking
        pause_offset = 0
        last_pause_time = 0
        
        # UI Elements
        font = pygame.font.Font(None, 24)
        reset_btn_rect = pygame.Rect(10, 10, 80, 30)
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                        if self.paused:
                            if self.audio_file: pygame.mixer.music.pause()
                            last_pause_time = time.time()
                        else:
                            if self.audio_file: pygame.mixer.music.unpause()
                            pause_offset += time.time() - last_pause_time
                    elif event.key == pygame.K_r:
                        self.reset_visualizer()
                        start_time = time.time()
                        pause_offset = 0
                        self.paused = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click
                        if reset_btn_rect.collidepoint(event.pos):
                            self.reset_visualizer()
                            start_time = time.time()
                            pause_offset = 0
                            self.paused = False
            
            if self.paused:
                # Draw paused state overlay
                pause_text = font.render("PAUSED", True, (255, 255, 255))
                text_rect = pause_text.get_rect(center=(self.screen_width/2, self.screen_height/2))
                self.screen.blit(pause_text, text_rect)
                pygame.display.flip()
                self.clock.tick(30)
                continue
                    
            # Calculate current time
            self.current_time = time.time() - start_time - pause_offset
            
            # Process MIDI events
            self.process_events()
            
            # Update and render
            self.update()
            self.draw()
            
            # Draw UI
            pygame.draw.rect(self.screen, (60, 60, 60), reset_btn_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), reset_btn_rect, 1)
            btn_text = font.render("RESET", True, (200, 200, 200))
            text_rect = btn_text.get_rect(center=reset_btn_rect.center)
            self.screen.blit(btn_text, text_rect)
            
            pygame.display.flip()
            
            # Cap framerate
            self.clock.tick(60)
            
        pygame.quit()
        
class VisualEffect:
    """Base class for visual effects"""
    def __init__(self):
        pass
        
    def trigger(self, event):
        """Trigger effect based on MIDI event"""
        pass
        
    def update(self):
        """Update effect state"""
        pass
        
    def render(self, screen):
        """Render effect to screen"""
        pass
        
    def reset(self):
        """Reset effect state"""
        pass
        
# General MIDI Drum Map Positions (normalized 0-1)
DRUM_POSITIONS = {
    # Kick
    35: (0.5, 0.85), 36: (0.5, 0.85),
    # Snare
    38: (0.4, 0.6), 40: (0.4, 0.6), 37: (0.4, 0.6),
    # Hi-Hat
    42: (0.2, 0.6), 44: (0.2, 0.65), 46: (0.2, 0.5),
    # Toms
    41: (0.75, 0.7), 43: (0.65, 0.55), 45: (0.5, 0.45), 
    47: (0.35, 0.55), 48: (0.3, 0.5), 50: (0.3, 0.5),
    # Cymbals
    49: (0.2, 0.3), 57: (0.8, 0.3), 52: (0.85, 0.25), 55: (0.15, 0.25),
    # Ride
    51: (0.7, 0.4), 59: (0.7, 0.4), 53: (0.65, 0.35)
}

class DrumHitEffect(VisualEffect):
    """Effect that flashes drums at specific positions"""
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.hits = []
        
    def reset(self):
        self.hits = []
        
    def trigger(self, event):
        """Trigger hit visualization"""
        if event['type'] == 'note_on' and event['velocity'] > 0:
            note = event['note']
            # Get position
            if note in DRUM_POSITIONS:
                pos = DRUM_POSITIONS[note]
                x, y = int(pos[0] * self.width), int(pos[1] * self.height)
            else:
                # Fallback for non-drum notes
                x = int((0.1 + ((note % 24) / 24.0) * 0.8) * self.width)
                y = int(self.height * 0.5)

            # Color based on note
            hue = (event['note'] % 12) / 12.0
            rgb = self.hsv_to_rgb(hue, 0.7, 1.0)
            color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
            
            self.hits.append({
                'x': x, 'y': y,
                'radius': 10,
                'max_radius': 30 + (event['velocity'] / 127) * 100,
                'color': color,
                'life': 1.0,
                'decay': 0.05
            })
            
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB color space"""
        if s == 0.0:
            return (v, v, v)
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        
        i = i % 6
        if i == 0:
            return (v, t, p)
        elif i == 1:
            return (q, v, p)
        elif i == 2:
            return (p, v, t)
        elif i == 3:
            return (p, q, v)
        elif i == 4:
            return (t, p, v)
        else:
            return (v, p, q)
            
    def update(self):
        """Update hits"""
        for hit in self.hits:
            hit['life'] -= hit['decay']
            hit['radius'] += (hit['max_radius'] - hit['radius']) * 0.2
            
        self.hits = [h for h in self.hits if h['life'] > 0]
        
    def render(self, screen):
        """Render hits"""
        for hit in self.hits:
            # Fade alpha
            alpha = int(hit['life'] * 255)
            color = hit['color']
            
            # Draw glow
            surf = pygame.Surface((int(hit['radius']*2), int(hit['radius']*2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*color, alpha), (int(hit['radius']), int(hit['radius'])), int(hit['radius']))
            screen.blit(surf, (hit['x'] - hit['radius'], hit['y'] - hit['radius']))
            
            # Draw core
            pygame.draw.circle(screen, (255, 255, 255), (hit['x'], hit['y']), int(hit['radius'] * 0.3 * hit['life']))
        
class ParticleEmitterEffect(VisualEffect):
    """Effect that emits particles based on MIDI events"""
    def __init__(self, width, height, max_particles=200):
        super().__init__()
        self.width = width
        self.height = height
        self.max_particles = max_particles
        self.particles = []
        
    def reset(self):
        self.particles = []
        
    def trigger(self, event):
        """Trigger particle emission based on MIDI event"""
        if event['type'] == 'note_on' and event['velocity'] > 0:
            # Create particles based on velocity
            num_particles = int((event['velocity'] / 127) * 50) + 10
            
            note = event['note']
            if note in DRUM_POSITIONS:
                pos = DRUM_POSITIONS[note]
                x, y = int(pos[0] * self.width), int(pos[1] * self.height)
            else:
                x = int((0.1 + ((note % 24) / 24.0) * 0.8) * self.width)
                y = int(self.height * 0.5)
            
            for _ in range(num_particles):
                if len(self.particles) < self.max_particles:
                    self.create_particle(x, y, event['note'])
                    
    def create_particle(self, x, y, note):
        """Create a new particle"""
        angle = np.random.rand() * 2 * np.pi
        speed = np.random.rand() * 3 + 1
        lifetime = np.random.rand() * 2 + 1
        
        # Map note to color
        hue = (note % 12) / 12.0
        rgb = self.hsv_to_rgb(hue, 0.8, 0.8)
        color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        
        particle = {
            'x': x,
            'y': y,
            'vx': np.cos(angle) * speed,
            'vy': np.sin(angle) * speed,
            'lifetime': lifetime,
            'max_lifetime': lifetime,
            'color': color,
            'size': np.random.rand() * 3 + 2
        }
        
        self.particles.append(particle)
        
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB color space"""
        if s == 0.0:
            return (v, v, v)
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        
        i = i % 6
        if i == 0:
            return (v, t, p)
        elif i == 1:
            return (q, v, p)
        elif i == 2:
            return (p, v, t)
        elif i == 3:
            return (p, q, v)
        elif i == 4:
            return (t, p, v)
        else:
            return (v, p, q)
            
    def update(self):
        """Update all particles"""
        # Update particles
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['lifetime'] -= 0.016  # Approx 60fps
            
        # Remove dead particles
        self.particles = [p for p in self.particles if p['lifetime'] > 0]
        
    def render(self, screen):
        """Render all particles"""
        for particle in self.particles:
            # Fade particles as they die
            alpha = int((particle['lifetime'] / particle['max_lifetime']) * 255)
            color = (particle['color'][0], particle['color'][1], particle['color'][2], alpha)
            
            # Create a surface for alpha blending
            surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (int(particle['size']), int(particle['size'])), int(particle['size']))
            
            screen.blit(surf, (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))
            
def main():
    parser = argparse.ArgumentParser(description="R# - MIDI Visualizer")
    parser.add_argument("midi_file", help="Path to input MIDI file")
    parser.add_argument("--bpm", "-b", type=int, default=120, help="BPM of the track")
    parser.add_argument("--audio", "-a", help="Path to audio file for playback")
    args = parser.parse_args()
    
    # Create R# instance
    rsharp = RSharp(args.midi_file, args.audio, args.bpm)
    
    # Add visual effects
    drum_hits = DrumHitEffect(rsharp.screen_width, rsharp.screen_height)
    particle_emitter = ParticleEmitterEffect(rsharp.screen_width, rsharp.screen_height)
    
    rsharp.add_visual_effect(drum_hits)
    rsharp.add_visual_effect(particle_emitter)
    
    # Run the visualizer
    print("Starting R# visualizer...")
    print("Press ESC or close the window to exit")
    rsharp.run()
    
if __name__ == "__main__":
    main()