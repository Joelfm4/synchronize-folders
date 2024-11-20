from src.tree_builder import *
from src.input_validation import validation
import src.synchronization_folders as sync
import copy

def main():
    # Get user inputs and verify them
    original_path, replica_path, interval, log_file_path = validation() 

    original_node:Node = build_tree(original_path)

    replica_node:Node = build_tree(replica_path)

    interval:int = interval 


    # First Sync
    if sync.replica_folder_existence(replica_path):
        sync.log_file_path = log_file_path
        sync.duplicate_original(original_node, replica_path)
        replica_node = copy.deepcopy(original_node)

    
    # Check for chances
    




if __name__ == "__main__":
    main()



























