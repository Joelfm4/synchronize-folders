import src.synchronization_folders as sync
from src.input_validation import validation
from src.watch_changes import FolderMonitor
import schedule
import logging
import time


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


def main():
    original_folder_path, replica_folder_path, interval, log_file_path = validation() 
    configure_logging(log_file_path)


    # Sync the replica folder if necessary #
    if sync.replica_folder_is_empty(replica_folder_path):
        sync.duplicate_original(original_folder_path, replica_folder_path) 

    else:
        sync.update_replica_folder(original_folder_path, replica_folder_path)


    # Start Monitoring #
    folder_monitor = FolderMonitor(original_folder_path)
    folder_monitor.start()

    try:
        while True:
            time.sleep(interval) # * 60
            
            changes = folder_monitor.get_changes()

            if changes:
               sync.synchronize(original_folder_path, replica_folder_path, changes)
            


    except KeyboardInterrupt:
        folder_monitor.stop()


if __name__ == "__main__":
    main()























