import argparse
import mido
import pygame
import numpy as np
import time
import sys

class RSharp:
    def __init__(self, midi_file, bpm=120):
        self.midi_file = midi_file
        self.bpm = bpm
        self.events = []
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
        
    def process_events(self):
        """Process MIDI events based on current time"""
        # Find all events that should be triggered now
        triggered_events = []
        event_indices = []
        
        for i, event in enumerate(self.events):
            if event['time'] <= self.current_time:
                triggered_events.append(event)
                event_indices.append(i)
            else:
                break
                
        # Remove processed events
        for i in reversed(event_indices):
            del self.events[i]
            
        # Trigger visual effects for each event
        for event in triggered_events:
            for effect in self.visual_effects:
                effect.trigger(event)
                
    def update(self):
        """Update all visual effects"""
        for effect in self.visual_effects:
            effect.update()
            
    def render(self):
        """Render all visual effects"""
        # Clear screen
        self.screen.fill((20, 20, 20))
        
        # Render effects
        for effect in self.visual_effects:
            effect.render(self.screen)
            
        # Update display
        pygame.display.flip()
        
    def run(self):
        """Main loop"""
        self.running = True
        start_time = time.time()
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            # Calculate current time
            self.current_time = time.time() - start_time
            
            # Process MIDI events
            self.process_events()
            
            # Update and render
            self.update()
            self.render()
            
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
        
class ColorChangerEffect(VisualEffect):
    """Effect that changes color based on MIDI events"""
    def __init__(self, center_x, center_y, base_color=(255, 0, 0), radius=100):
        super().__init__()
        self.center_x = center_x
        self.center_y = center_y
        self.base_color = base_color
        self.radius = radius
        self.current_color = base_color
        self.target_color = base_color
        self.fade_speed = 0.02
        
    def trigger(self, event):
        """Trigger color change based on MIDI event"""
        if event['type'] == 'note_on':
            # Map note number to color
            hue = (event['note'] % 12) / 12.0
            rgb = self.hsv_to_rgb(hue, 0.8, 0.8)
            self.target_color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
            
            # Map velocity to radius
            self.radius = 50 + (event['velocity'] / 127) * 150
            
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
        """Fade current color to target color"""
        # Fade current color towards target color
        r = self.current_color[0] + (self.target_color[0] - self.current_color[0]) * self.fade_speed
        g = self.current_color[1] + (self.target_color[1] - self.current_color[1]) * self.fade_speed
        b = self.current_color[2] + (self.target_color[2] - self.current_color[2]) * self.fade_speed
        
        self.current_color = (int(r), int(g), int(b))
        
    def render(self, screen):
        """Render the color changing circle"""
        pygame.draw.circle(screen, self.current_color, 
                         (self.center_x, self.center_y), self.radius)
        
class ParticleEmitterEffect(VisualEffect):
    """Effect that emits particles based on MIDI events"""
    def __init__(self, center_x, center_y, max_particles=200):
        super().__init__()
        self.center_x = center_x
        self.center_y = center_y
        self.max_particles = max_particles
        self.particles = []
        
    def trigger(self, event):
        """Trigger particle emission based on MIDI event"""
        if event['type'] == 'note_on':
            # Create particles based on velocity
            num_particles = int((event['velocity'] / 127) * 50) + 10
            
            for _ in range(num_particles):
                if len(self.particles) < self.max_particles:
                    self.create_particle(event['note'])
                    
    def create_particle(self, note):
        """Create a new particle"""
        angle = np.random.rand() * 2 * np.pi
        speed = np.random.rand() * 3 + 1
        lifetime = np.random.rand() * 2 + 1
        
        # Map note to color
        hue = (note % 12) / 12.0
        rgb = self.hsv_to_rgb(hue, 0.8, 0.8)
        color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        
        particle = {
            'x': self.center_x,
            'y': self.center_y,
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
    args = parser.parse_args()
    
    # Create R# instance
    rsharp = RSharp(args.midi_file, args.bpm)
    
    # Add visual effects
    color_changer = ColorChangerEffect(rsharp.screen_width // 2, rsharp.screen_height // 2)
    particle_emitter = ParticleEmitterEffect(rsharp.screen_width // 2, rsharp.screen_height // 2)
    
    rsharp.add_visual_effect(color_changer)
    rsharp.add_visual_effect(particle_emitter)
    
    # Run the visualizer
    print("Starting R# visualizer...")
    print("Press ESC or close the window to exit")
    rsharp.run()
    
if __name__ == "__main__":
    main()