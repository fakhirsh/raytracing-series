#!/usr/bin/env python3
"""
Live Preview Tool for PPM/image generation scripts.
This watches your pattern file and displays it with hot reload.

Usage: python live_preview.py your_pattern.py
"""

import sys
import time
import importlib.util
import os
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import io
import contextlib

class PatternRunner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.module_name = Path(filepath).stem
        
    def load_and_run(self):
        """Load the pattern file and capture its PPM output"""
        # Load the module
        spec = importlib.util.spec_from_file_location(self.module_name, self.filepath)
        module = importlib.util.module_from_spec(spec)
        
        # Capture stdout
        captured_output = io.StringIO()
        
        # Execute the module and capture its print output
        with contextlib.redirect_stdout(captured_output):
            spec.loader.exec_module(module)
            
            # If it has a main() function, call it
            if hasattr(module, 'main'):
                module.main()
        
        # Parse the PPM output
        ppm_text = captured_output.getvalue()
        return self.parse_ppm(ppm_text)
    
    def parse_ppm(self, ppm_text):
        """Parse PPM P3 format text into a PIL Image"""
        lines = ppm_text.strip().split('\n')
        if not lines or not lines[0].startswith('P3'):
            raise ValueError("Not a valid PPM P3 format")
        
        # Parse header
        idx = 1
        while idx < len(lines) and lines[idx].startswith('#'):
            idx += 1  # Skip comments
        
        # Get dimensions
        dimensions = lines[idx].split()
        width, height = int(dimensions[0]), int(dimensions[1])
        idx += 1
        
        # Get max value (usually 255)
        max_val = int(lines[idx])
        idx += 1
        
        # Parse pixel data
        pixels = []
        for line in lines[idx:]:
            values = line.split()
            pixels.extend([int(v) for v in values])
        
        # Create image
        img = Image.new('RGB', (width, height))
        pixel_data = []
        for i in range(0, len(pixels), 3):
            pixel_data.append((pixels[i], pixels[i+1], pixels[i+2]))
        
        img.putdata(pixel_data)
        return img

class LivePreviewWindow:
    def __init__(self, pattern_file):
        self.pattern_file = pattern_file
        self.runner = PatternRunner(pattern_file)
        
        # Create window
        self.root = tk.Tk()
        self.root.title(f"Live Preview: {Path(pattern_file).name}")
        
        # Create label for image
        self.label = tk.Label(self.root)
        self.label.pack()
        
        # Status label
        self.status = tk.Label(self.root, text="", fg="gray")
        self.status.pack()
        
        # Initial load
        self.update_image()
    
    def update_image(self):
        """Reload the pattern file and update display"""
        try:
            img = self.runner.load_and_run()
            photo = ImageTk.PhotoImage(img)
            self.label.configure(image=photo)
            self.label.image = photo  # Keep reference
            self.status.config(text=f"Updated: {time.strftime('%H:%M:%S')}", fg="green")
            print(f"✓ Image updated at {time.strftime('%H:%M:%S')}")
        except Exception as e:
            self.status.config(text=f"Error: {str(e)}", fg="red")
            print(f"✗ Error: {e}")
    
    def run(self):
        self.root.mainloop()

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, window):
        self.window = window
        self.last_modified = 0
    
    def on_modified(self, event):
        # Check if it's our watched file
        if not event.is_directory and event.src_path.endswith(self.window.pattern_file):
            # Debounce rapid changes
            current_time = time.time()
            if current_time - self.last_modified < 0.5:
                return
            self.last_modified = current_time
            
            # Update in GUI thread
            self.window.root.after(10, self.window.update_image)

def main():
    if len(sys.argv) < 2:
        print("Usage: python live_preview.py your_pattern.py")
        print("\nThis will watch your pattern file and display its PPM output with hot reload.")
        sys.exit(1)
    
    pattern_file = sys.argv[1]
    
    if not os.path.exists(pattern_file):
        print(f"Error: File '{pattern_file}' not found")
        sys.exit(1)
    
    print(f"Starting live preview for: {pattern_file}")
    print("The window will update automatically when you save changes.")
    print("Press Ctrl+C in terminal or close the window to exit.\n")
    
    # Create window
    window = LivePreviewWindow(pattern_file)
    
    # Set up file watcher
    event_handler = FileChangeHandler(window)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(pattern_file) or '.', recursive=False)
    observer.start()
    
    try:
        window.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()