from multiprocessing import Process, Queue, Event
from typing import List, Optional
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
import os
import time


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, event_queue:Queue):
        super().__init__()
        self.event_queue = event_queue

    def on_created(self, event:FileSystemEvent) -> None:
        print(event)
        if event.is_directory:
            print("Created Folder")
            self._add_event("created", event, is_file=False)
        else:
            print("Created File")
            self._add_event("created", event, is_file=True)


    def on_deleted(self, event:FileSystemEvent) -> None:
        print(event)
        if event.is_directory:
            print("Deleted Folder")
            self._add_event("deleted", event, is_file=False)
        else:
            print("Deleted File")
            self._add_event("deleted", event, is_file=True)


    def on_modified(self, event:FileSystemEvent) -> None:
        if not event.is_directory:
            print("File Edited")
            self._add_event("modified", event, is_file=True)


    def on_moved(self, event: FileSystemEvent) -> None:
        src_parent: str = os.path.dirname(event.src_path)
        dest_parent: str = os.path.dirname(event.dest_path)
        
        print(event)
        # Rename
        if src_parent == dest_parent:
            if event.is_directory:
                print("Renamed Folder")
                norm_dest = os.path.normpath(event.dest_path)

                self._add_event("renamed", event, norm_dest,is_file=False)

            else:
                print("Renamed File")
                self._add_event("renamed", event, is_file=True)

        # Move
        else:
            if event.is_directory:
                print("Moved Folder")
                self._add_event("Moved", event, new_path=dest_parent,is_file=False)
            else:
                print("Moved File")
                self._add_event("Moved", event, is_file=True)


    def _add_event(self, event_type: str, event: FileSystemEvent, new_path: Optional[str] = None, is_file: bool = False) -> None:
        self.event_queue.put({
            "type": event_type,
            "path": os.path.normpath(event.src_path),
            "new_path": new_path,
            "is_file": is_file,
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
    path_to_monitor = "D:/Root"
    folder_monitor = FolderMonitor(os.path.normpath(path_to_monitor))
    folder_monitor.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        folder_monitor.stop()
   
