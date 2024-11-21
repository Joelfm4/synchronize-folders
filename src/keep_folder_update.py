from multiprocessing.context import Process
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer 
from multiprocessing import Process, Queue
import os
import time

class MyHandler(FileSystemEventHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_modified(self, event) -> None:
        print(f"Modify: {os.path.normpath(event.src_path)}")

    def on_created(self, event) -> None:
        print(f"Created: {os.path.normpath(event.src_path)}")

    def on_deleted(self, event) -> None:
        print(f"Deleted: {os.path.normpath(event.src_path)}")



def folder_monitoring(path) -> None:
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def start_folder_monitoring(path:str) -> Process:
    monitor_process = multiprocessing.Process(target=folder_monitoring, args=(path,), daemon=True)
    monitor_process.start()

    return monitor_process


def pausa_folder_monitoring():
    ...


if __name__ == "__main__":
    path = "D:/Root"
    start_folder_monitoring(path)



