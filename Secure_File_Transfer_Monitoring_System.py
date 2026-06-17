import os
import time
import hashlib
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ==============================
# Configuration
# ==============================

MONITORED_DIRECTORY = "."

SENSITIVE_DIRECTORIES = [
    "./secret"
]

LOG_FILE = "file_transfer_log.txt"

# debounce settings (prevents event spam)
EVENT_DELAY = 1
last_event = {}

# ==============================
# Logging Setup
# ==============================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

# ==============================
# Hash Function
# ==============================

def calculate_hash(file_path):

    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()

    except Exception:
        return None


# ==============================
# Authorization Check
# ==============================

def is_sensitive(path):

    path = os.path.abspath(path)

    for directory in SENSITIVE_DIRECTORIES:
        if path.startswith(os.path.abspath(directory)):
            return True

    return False


# ==============================
# Event Deduplication
# ==============================

def should_ignore(file_path):

    now = time.time()

    if file_path in last_event:
        if now - last_event[file_path] < EVENT_DELAY:
            return True

    last_event[file_path] = now
    return False


# ==============================
# File Event Handler
# ==============================

class FileMonitorHandler(FileSystemEventHandler):

    def process(self, event_type, file_path, dest=None):

        if LOG_FILE in file_path:
            return

        if should_ignore(file_path):
            return

        file_hash = calculate_hash(file_path) if os.path.exists(file_path) else None

        if event_type == "created":

            if is_sensitive(file_path):
                alert = f"ALERT: Sensitive file created -> {file_path}"
                print(alert)
                logging.warning(alert)

            log = f"FILE CREATED | Path: {file_path} | Hash: {file_hash}"

        elif event_type == "modified":

            log = f"FILE MODIFIED | Path: {file_path} | Hash: {file_hash}"

        elif event_type == "deleted":

            log = f"FILE DELETED | Path: {file_path}"

        elif event_type == "moved":

            if is_sensitive(file_path):
                alert = f"ALERT: Sensitive file moved -> {file_path} to {dest}"
                print(alert)
                logging.warning(alert)

            log = f"FILE MOVED | From: {file_path} | To: {dest}"

        else:
            return

        print(log)
        logging.info(log)


    def on_created(self, event):
        if not event.is_directory:
            self.process("created", event.src_path)


    def on_modified(self, event):
        if not event.is_directory:
            self.process("modified", event.src_path)


    def on_deleted(self, event):
        if not event.is_directory:
            self.process("deleted", event.src_path)


    def on_moved(self, event):
        if not event.is_directory:
            self.process("moved", event.src_path, event.dest_path)


# ==============================
# Monitor Start
# ==============================

def start_monitoring():

    if not os.path.exists(MONITORED_DIRECTORY):
        os.makedirs(MONITORED_DIRECTORY)

    event_handler = FileMonitorHandler()

    observer = Observer()
    observer.schedule(event_handler, MONITORED_DIRECTORY, recursive=True)

    observer.start()

    print("Monitoring Started...")
    print(f"Watching directory: {os.path.abspath(MONITORED_DIRECTORY)}")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


# ==============================
# Main
# ==============================

if __name__ == "__main__":
    start_monitoring()
