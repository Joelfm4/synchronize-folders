from multiprocessing import Process, Queue, Event
from typing import List
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
import os
import time


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, event_queue:Queue):
        super().__init__()
        self.event_queue = event_queue


    def on_created(self, event:FileSystemEvent) -> None:
        if event.is_directory:
            self._add_event("created", event, is_file=False)

        else:
            self._add_event("created", event, is_file=True)


    def on_deleted(self, event:FileSystemEvent) -> None:
        if event.is_directory:
            self._add_event("deleted", event, is_file=False)
        else:
            self._add_event("deleted", event, is_file=True)


    def on_modified(self, event:FileSystemEvent) -> None:
        if not event.is_directory:
            self._add_event("modified", event, is_file=True)


    def on_moved(self, event:FileSystemEvent) -> None:
        if event.is_directory:
            self._add_event("moved", event, is_file=False)
        else:
            self._add_event("moved", event, is_file=True)


    def _add_event(self, event_type:str, event:FileSystemEvent, is_file:bool) -> None:
        self.event_queue.put({
            "type": event_type,
            "path": os.path.normpath(event.src_path),
            "is_file": is_file 
        })



def folder_monitoring(path:str, event_queue:Queue, stop_event:Event) -> None:
    event_handler:MyEventHandler = MyEventHandler(event_queue) 

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


    def start(self) -> None:
        if not self.process or not self.process.is_alive():
            self.process = Process(
                target=folder_monitoring,
                args=(self.path, self.event_queue, self.stop_event),
                daemon=True
            )
            self.process.start()


    def stop(self) -> None:
        if self.process and self.process.is_alive():
            self.stop_event.set()
            self.process.join()


    def get_changes(self) -> List[dict]:
        changes = []
        while not self.event_queue.empty():
            changes.append(self.event_queue.get())
        return changes



if __name__ == "__main__":
    path_to_monitor = ""
    folder_monitor = FolderMonitor(path_to_monitor)
    folder_monitor.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        folder_monitor.stop()
   

"""
def process_events(changes) -> list:
    processed = {}

    for change in changes:
        path = change["path"]
        if change["type"] == "Deleted":
            processed[path] = change  
        elif path not in processed or processed[path]["type"] != "Deleted":
            processed[path] = change 

    return list(processed.values())


def main():
    original_folder_path, replica_folder_path, interval, log_file_path = validation() 
    configure_logging(log_file_path)


    # Sync the replica folder if necessary
    if sync.replica_folder_is_empty(replica_folder_path):
        sync.duplicate_original(original_folder_path, replica_folder_path) 

    else:
        sync.update_replica_folder(original_folder_path, replica_folder_path)


    # Start Monitoring 
    folder_monitor = FolderMonitor(original_folder_path)
    folder_monitor.start()

    try:
        while True:
            time.sleep(interval )
            sync.update_replica_folder(original_folder_path, replica_folder_path)

            changes = folder_monitor.get_changes()

            if changes:
                changes = process_events(changes)
                print(changes)
                # folder_monitor.stop()
                # sync.synchronize(original_folder_path, replica_folder_path, changes)
            
            folder_monitor.get_changes()


    except KeyboardInterrupt:
        folder_monitor.stop()
    finally:
        folder_monitor.stop()

"""
