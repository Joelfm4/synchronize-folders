import os
import shutil
import concurrent.futures
import logging
logger = logging.getLogger(__name__)


log_file_path:str = ""
logging.basicConfig(filename=log_file_path, level=logging.INFO)


# Check if the replica folder is empty -> True = Empty
def replica_folder_existence(replica_path:str) -> bool:
    return len(os.listdir(replica_path)) == 0


def duplicate_original(original_node, replica_path:str) -> None:

    # Depth-First Traversals - Pre-order
    if original_node.is_file:
        dest_file_path = os.path.join(replica_path, original_node.name)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            task = executor.submit(shutil.copyfile, original_node.path, dest_file_path)
            task.result()
            logger.info(f"File Created: {original_node.name}")

    else:
        new_dest_dir = os.path.normpath(os.path.join(replica_path, original_node.name))
        
        if not os.path.exists(new_dest_dir):
            os.makedirs(new_dest_dir) 
            logger.info(f"Folder Created: {original_node.name}")
        
        for child in original_node.children:
            duplicate_original(child, new_dest_dir)
        


def synchronize(main_folder_tree, replica_folder_tree):
     ...





if __name__ == "__main__":
    ...

# Original comparator with replica

# Cases:
# If the replica is empty just copy the original tree
# The file is not on original - Delete It
# The file has been changed - Add or Edit
# The File is updated - Pass

# Notes
# First - Check father timestemp
# After check and confirm that has been edited go ahead



