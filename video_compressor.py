import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import subprocess

def compress_video(input_path, output_path, target_size_mb):
    """Compress the video to be smaller than or equal to target_size_mb using FFmpeg."""
    target_size_bytes = target_size_mb * 1024 * 1024  # Convert MB to bytes

    # Use FFmpeg to compress the video
    command = [
        "ffmpeg", 
        "-i", input_path, 
        "-b:v", "1000k",  # Example bitrate, adjust as necessary
        "-maxrate", "1000k",
        "-bufsize", "2000k",
        "-vf", "scale=-2:720",  # Example scaling; adjust as necessary
        output_path
    ]

    # Execute the command
    subprocess.run(command, check=True)

    # Check output file size and adjust if necessary
    if os.path.getsize(output_path) > target_size_bytes:
        print(f"Warning: Output file '{output_path}' is larger than {target_size_mb} MB.")


def find_next_clip_name(folder_path):
    """Find the next available 'Clip (n)' name in the target folder."""
    existing_clips = [f for f in os.listdir(folder_path) if f.startswith("Clip") and f.endswith(".mp4")]
    
    max_num = 0
    for clip_name in existing_clips:
        num = clip_name.split("(")[-1].split(")")[0]
        try:
            max_num = max(max_num, int(num))
        except ValueError:
            continue
    
    return f"Clip ({max_num + 1}).mp4"

def process_file(file_path, output_folder, target_size_mb=25):
    """Process a single file, compress it, rename and move to target folder."""
    if file_path.endswith(".mp4") and "trim" in file_path.lower():
        next_clip_name = find_next_clip_name(output_folder)
        output_file_path = os.path.join(output_folder, next_clip_name)

        print(f"Compressing and renaming '{file_path}' to '{next_clip_name}'...")
        compress_video(file_path, output_file_path, target_size_mb)

class Watcher:
    def __init__(self, input_folder, output_folder, target_size_mb=25):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.target_size_mb = target_size_mb
        self.event_handler = FileSystemEventHandler()
        self.event_handler.on_created = self.on_created
        self.observer = Observer()

    def on_created(self, event):
        # Process only if a file is created
        if not event.is_directory and event.src_path.endswith(".mp4") and "trim" in event.src_path.lower():
            print(f"New file detected: {event.src_path}")
            process_file(event.src_path, self.output_folder, self.target_size_mb)

    def start(self):
        print(f"Monitoring folder: {self.input_folder}")
        self.observer.schedule(self.event_handler, self.input_folder, recursive=False)
        self.observer.start()

        try:
            while True:
                time.sleep(1)  # Keeps the script running
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()

# Example usage
if __name__ == "__main__":
    input_folder = "input_folder"
    output_folder = "clips_folder"
    
    watcher = Watcher(input_folder, output_folder)
    watcher.start()
