import os
import shutil
import concurrent.futures
import logging
from typing import List
logger = logging.getLogger(__name__)


log_file_path:str = ""

FORMAT = '%(levelname)s - %(asctime)s - %(message)s'
DATEFMT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(
    format=FORMAT,
    datefmt=DATEFMT,
    filename=log_file_path,
    level=logging.INFO
)


def replica_folder_is_empty(replica_path:str) -> bool:
    return len(os.listdir(replica_path)) == 0


def duplicate_original(original_folder_path:str, replica_folder_path:str) -> None:
    if not os.path.exists(replica_folder_path):
        os.makedirs(replica_folder_path)
        # LOG HERE FOLDER CREATED
        print(f"Created folder: {replica_folder_path}")

    def copy_item(item_path: str, base_original: str, base_replica: str) -> None:
        relative_path = os.path.relpath(path=item_path, start=base_original)
        target_path = os.path.join(base_replica, relative_path)

        if os.path.isdir(item_path):
            if not os.path.exists(target_path):
                os.makedirs(target_path)
                # LOG HERE FOLDER CREATED
                print(f"Created folder: {target_path}")
        else:
            shutil.copy2(item_path, target_path)
            # LOG HERE FILE COPIED
            print(f"Copied file: {item_path} -> {target_path}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for root, dirs, files in os.walk(original_folder_path):
            for name in dirs + files:
                item_path = os.path.join(root, name)
                futures.append(executor.submit(copy_item, item_path, original_folder_path, replica_folder_path))
        
        concurrent.futures.wait(futures)        


def copy_file(original_file: str, replica_file: str) -> None:
    replica_dir = os.path.dirname(replica_file)
    if not os.path.exists(path=replica_dir):
        os.makedirs(replica_dir)

    shutil.copy2(src=original_file, dst=replica_file)
    print(f"Copied: {original_file} -> {replica_file}")  # LOG


def delete_extra_files(replica_path: str) -> None:
    if os.path.isfile(replica_path):
        os.remove(path=replica_path)
        print(f"Deleted file: {replica_path}")  # LOG

    elif os.path.isdir(replica_path):
        shutil.rmtree(path=replica_path)
        print(f"Deleted folder: {replica_path}")  # LOG


def update_replica_folder(original_folder_path: str, replica_folder_path: str) -> None:

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures:List[concurrent.futures.Future] = []
        
        # Loop through the original folder and update the replica
        for root, dirs, files in os.walk(original_folder_path, topdown=True):
            for dir in dirs:
                original_dir = os.path.join(root, dir)
                relative_path = os.path.relpath(path=original_dir, start=original_folder_path)
                replica_dir = os.path.join(replica_folder_path, relative_path)
                
                if not os.path.exists(replica_dir):
                    os.makedirs(replica_dir)
                    print(f"Created directory: {replica_dir}")  # LOG

                if os.stat(original_dir).st_mtime > os.stat(replica_dir).st_mtime:
                    futures.append(executor.submit(copy_file, original_dir, replica_dir))

            for file in files:
                original_file = os.path.join(root, file)
                relative_path = os.path.relpath(path=original_file, start=original_folder_path)
                replica_file = os.path.join(replica_folder_path, relative_path)

                if not os.path.exists(replica_file) or os.stat(original_file).st_mtime > os.stat(replica_file).st_mtime:
                    futures.append(executor.submit(copy_file, original_file, replica_file))

                    
        # Search for files that do not match the original
        for root, dirs, files in os.walk(replica_folder_path, topdown=False):
            for name in files:
                replica_file = os.path.join(root, name)
                original_file = os.path.join(original_folder_path, os.path.relpath(path=replica_file, start=replica_folder_path))
                if not os.path.exists(original_file):
                    futures.append(executor.submit(delete_extra_files, replica_file))

            for name in dirs:
                replica_dir = os.path.join(root, name)
                original_dir = os.path.join(original_folder_path, os.path.relpath(path=replica_dir, start=replica_folder_path))
                if not os.path.exists(original_dir):
                    futures.append(executor.submit(delete_extra_files, replica_dir))

        concurrent.futures.wait(futures)



def synchronize(main_folder_tree, replica_folder_tree):
     ...





if __name__ == "__main__":
    ...

