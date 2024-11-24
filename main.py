from src.input_validation import validation
from src.watch_changes import FolderMonitor
from src.synchronization import *
import logging
import time
import sys 
import os


def configure_logging(log_file_path):
    logging.basicConfig(
        filename=log_file_path,
        format='%(levelname)s - %(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger()
    logger.addHandler(console_handler)




def filter_changes(changes):
    tmp = []

    for change in changes:
        if change['type'] in ['created', 'modified'] and os.path.basename(change['path']).startswith('.'):
            continue
        elif change['type'] == 'renamed' and os.path.basename(change['path']).startswith('.'):
            edited_change = {
                'type':'modified',
                'path': change['new_path'],
                'new_path': change['new_path'],
                'is_file': change['is_file'],
            }
            tmp.append(edited_change) 
    
        else:
            tmp.append(change)

    return tmp


def main() -> None:
    source_directory_path, replica_directory_path, interval, log_file_path = validation() 
    configure_logging(log_file_path)

    if source_directory_not_empty(source_directory_path):
        if replica_directory_is_empty(replica_directory_path):
            duplicate_source(source_directory_path, replica_directory_path) 
        else:
            update_replica_directory(source_directory_path, replica_directory_path)


    directory_monitor = FolderMonitor(source_directory_path)
    directory_monitor.start()

    try:
        while True:
            time.sleep(interval*60)
            
            changes = directory_monitor.get_changes()

            if changes:
                changes = filter_changes(changes)
                synchronize(source_directory_path, replica_directory_path, changes)

    except KeyboardInterrupt:
        directory_monitor.stop()
        update_replica_directory(source_directory_path, replica_directory_path)
        sys.exit(0)



if __name__ == "__main__":
    main()























