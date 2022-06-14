from django.conf import settings
from django.core.management.base import BaseCommand
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pathlib import Path

import time

class Command(BaseCommand):
    help = 'Watch for changes and touch a file'
    last_restarted = 0
    restart_delay = 100     # Min-time between restarts (stops duplicate restarts)
    go_recursively = True

    def current_milli_time(self):
        return int(round(time.time() * 1000))
    
    def touch(self, message):
        if not self.last_restarted:
            self.last_restarted = self.current_milli_time()
        elif self.last_restarted+self.restart_delay < self.current_milli_time():
            self.last_restarted = self.current_milli_time()
            if (settings.TOUCHWATCH_PATH):
                Path(settings.TOUCHWATCH_PATH).touch()
            if (settings.TOUCHWATCH_COMMAND):
                import os
                os.system(settings.TOUCHWATCH_COMMAND)
            self.stdout.write(message)
    
    def on_created(self, event):
        self.touch(f"RESTARTING: {event.src_path} has been created!")

    def on_deleted(self, event):
        self.stdout.write(f"NOTICE: File deleted {event.src_path}")

    def on_modified(self, event):
        self.touch(f"RESTARTING: {event.src_path} has been modified")

    def on_moved(self, event):
        self.stdout.write(f"NOTICE: File moved {event.src_path} to {event.dest_path}")

    def handle(self, *args, **kwargs):
        self.last_restarted = self.current_milli_time()

        # Settings check
        if settings.TOUCHWATCH_FOLDER == None:
            self.stdout.write(f"SETTINGS ERROR: Please set your 'TOUCHWATCH_FOLDER' setting.")
            exit;
        if settings.TOUCHWATCH_PATH == None and settings.TOUCHWATCH_COMMAND == None:
            self.stdout.write(f"SETTINGS ERROR: Please set your 'TOUCHWATCH_PATH' or 'TOUCHWATCH_COMMAND' setting.")
            exit;
        
        patterns = settings.TOUCHWATCH_PATTERN
        ignore_patterns = settings.TOUCHWATCH_IGNORE_PATTERN
        ignore_directories = settings.TOUCHWATCH_IGNORE_DIRECTORIES
        case_sensitive = settings.TOUCHWATCH_CASESENSITIVE
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

        my_event_handler.on_created = self.on_created
        my_event_handler.on_deleted = self.on_deleted
        my_event_handler.on_modified = self.on_modified
        my_event_handler.on_moved = self.on_moved

        my_observer = Observer()
        my_observer.schedule(my_event_handler, settings.TOUCHWATCH_FOLDER, recursive=self.go_recursively)
        my_observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()