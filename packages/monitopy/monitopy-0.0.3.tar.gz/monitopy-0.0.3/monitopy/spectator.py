import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileWatcher:
    def __init__(self, path, callback=None):
        self.path = path
        self.callback = callback
        self.event_handler = FileSystemEventHandler()
        self.event_handler.on_any_event = self.on_event
        self.observer = Observer()

    def on_event(self, event):
        if self.callback:
            self.callback(event)

    def start(self):
        self.observer.schedule(self.event_handler, path=self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.observer.stop()
        self.observer.join()