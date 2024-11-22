from multiprocessing import Process, Queue, Event
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import os
import time


class MyHandler(FileSystemEventHandler):
    def __init__(self, event_queue):
        super().__init__()
        self.event_queue = event_queue

    def on_modified(self, event):
        self._add_event("Modified", event)

    def on_created(self, event):
        self._add_event("Created", event)

    def on_deleted(self, event):
        self._add_event("Deleted", event)

    def _add_event(self, event_type, event):
        self.event_queue.put({
            "type": event_type,
            "path": os.path.normpath(event.src_path),
        })


def folder_monitoring(path, event_queue, stop_event):
    event_handler = MyHandler(event_queue)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while not stop_event.is_set():
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


class FolderMonitor:
    def __init__(self, path: str):
        self.path = path
        self.event_queue = Queue()
        self.stop_event = Event()
        self.process = None


    def start(self):
        if not self.process or not self.process.is_alive():
            self.process = Process(
                target=folder_monitoring,
                args=(self.path, self.event_queue, self.stop_event),
                daemon=True
            )
            self.process.start()


    def stop(self):
        if self.process and self.process.is_alive():
            self.stop_event.set()
            self.process.join()


    def get_changes(self):
        changes = []
        while not self.event_queue.empty():
            changes.append(self.event_queue.get())
        return changes



if __name__ == "__main__":
    path_to_monitor = "D:/Root"
    monitor = FolderMonitor(path_to_monitor)
    monitor.start()

    try:
        while True:
            time.sleep(10)
            changes = monitor.get_changes()
            if changes:
                for change in changes:
                    print(change)
    except KeyboardInterrupt:
        monitor.stop()

