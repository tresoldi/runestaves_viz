#!/usr/bin/env python3
"""
Watch for file changes and auto-rebuild site.

Monitors:
- scripts/
- templates/
- static/
- i18n/

On change, runs: make site-build
"""

import subprocess
import sys
import time
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("ERROR: watchdog not installed. Run: pip install watchdog")
    sys.exit(1)


class RebuildHandler(FileSystemEventHandler):
    """Handle file system events by triggering rebuild."""

    def __init__(self):
        self.last_rebuild = 0
        self.debounce_seconds = 1

    def on_modified(self, event):
        if event.is_directory:
            return

        # Debounce rapid changes
        now = time.time()
        if now - self.last_rebuild < self.debounce_seconds:
            return

        # Ignore generated files and temporary files
        if any(
            part in event.src_path
            for part in ['.git', '__pycache__', '.pyc', 'site/', 'venv/']
        ):
            return

        print(f"\n{'=' * 60}")
        print(f"File changed: {event.src_path}")
        print("Rebuilding site...")
        print('=' * 60)

        try:
            result = subprocess.run(['make', 'site-build'], check=True, capture_output=True, text=True)
            print(result.stdout)
            print("\n✓ Rebuild complete")
            self.last_rebuild = now
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Rebuild failed:")
            print(e.stderr)


def main():
    project_root = Path(__file__).parent.parent

    # Directories to watch
    watch_dirs = [
        project_root / 'scripts',
        project_root / 'templates',
        project_root / 'static',
        project_root / 'i18n',
    ]

    print("Starting file watcher...")
    print(f"Monitoring: {', '.join(str(d.name) for d in watch_dirs)}")
    print("Press Ctrl+C to stop\n")

    event_handler = RebuildHandler()
    observer = Observer()

    for watch_dir in watch_dirs:
        if watch_dir.exists():
            observer.schedule(event_handler, str(watch_dir), recursive=True)
            print(f"  ✓ Watching {watch_dir.relative_to(project_root)}")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping watcher...")
        observer.stop()

    observer.join()
    print("✓ Stopped")


if __name__ == '__main__':
    main()
