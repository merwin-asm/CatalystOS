import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# List of directories to monitor
DIRECTORIES_TO_MONITOR = ['/path/to/dir1', '/path/to/dir2']
TEMP_FILES_DIR = '/temp_files'
INTERVAL = 1  # Time interval for checking changes (in seconds)

# Ensure the temp_files directory exists
if not os.path.exists(TEMP_FILES_DIR):
    os.makedirs(TEMP_FILES_DIR)

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
    
    def on_modified(self, event):
        self._handle_event(event)
    
    def on_created(self, event):
        self._handle_event(event)
    
    def on_deleted(self, event):
        self._handle_event(event)
    
    def _handle_event(self, event):
        # Get the relative path of the file
        relative_path = os.path.relpath(event.src_path, start=os.path.commonpath(DIRECTORIES_TO_MONITOR))
        temp_file_path = os.path.join(TEMP_FILES_DIR, relative_path)
        
        if event.event_type in ['created', 'modified']:
            # Make sure the directory structure exists
            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
            shutil.copy2(event.src_path, temp_file_path)
            print(f"File {event.src_path} {event.event_type} and copied to {temp_file_path}")
        elif event.event_type == 'deleted':
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                print(f"File {event.src_path} {event.event_type} and removed from {temp_file_path}")

def apply_changes():
    for root, dirs, files in os.walk(TEMP_FILES_DIR):
        for file in files:
            temp_file_path = os.path.join(root, file)
            # Compute original file path
            original_file_path = os.path.join(DIRECTORIES_TO_MONITOR[0], os.path.relpath(temp_file_path, TEMP_FILES_DIR))
            # Ensure directory exists
            os.makedirs(os.path.dirname(original_file_path), exist_ok=True)
            # Copy file back to the original location
            shutil.copy2(temp_file_path, original_file_path)
            print(f"Applied change from {temp_file_path} to {original_file_path}")

def main():
    event_handler = ChangeHandler()
    observer = Observer()
    
    for directory in DIRECTORIES_TO_MONITOR:
        observer.schedule(event_handler, directory, recursive=True)
    
    observer.start()
    print("Monitoring started...")

    try:
        while True:
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Apply changes from temp_files to the monitored directories at startup
    apply_changes()
    # Start monitoring
    main()
