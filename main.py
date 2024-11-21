from src.input_validation import validation
import src.synchronization_folders as sync
from src.keep_folder_update import start_folder_monitoring 


def main():
    original_folder_path, replica_folder_path, interval, log_file_path = validation() 

    interval:int = interval 
    sync.log_file_path = log_file_path

    if sync.replica_folder_is_empty(replica_folder_path):
        sync.duplicate_original(original_folder_path, replica_folder_path) 

    else:
        sync.update_replica_folder(original_folder_path, replica_folder_path)

    




if __name__ == "__main__":
    main()



























