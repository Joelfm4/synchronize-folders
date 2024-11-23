import os
import shutil
import concurrent.futures
import logging
from typing import List

logger = logging.getLogger(__name__)


def replica_folder_is_empty(replica_path:str) -> bool:
    return len(os.listdir(replica_path)) == 0


def copy_file(original_path: str, replica_path: str) -> None:
    if os.path.isfile(original_path):
        shutil.copy2(src=original_path, dst=replica_path) 
        logging.info(f"[COPIED] File: {original_path} -> {replica_path}")

    else:
        shutil.copy2(src=original_path, dst=replica_path) 
        logging.info(f"[COPIED] Folder: {original_path} -> {replica_path}")


def delete_extra_files(replica_path: str) -> None:
    if os.path.isfile(replica_path):
        os.remove(path=replica_path)
        logging.info(f"[DELETED] File: {replica_path}")

    elif os.path.isdir(replica_path):
        shutil.rmtree(path=replica_path)
        logging.info(f"[DELETED] Folder: {replica_path}")


def duplicate_original(original_folder_path:str, replica_folder_path:str) -> None:
    if not os.path.exists(replica_folder_path):
        os.makedirs(replica_folder_path)
        logging.info(f"[CREATED] Folder: {replica_folder_path}")


    def copy_item(item_path: str, base_original: str, base_replica: str) -> None:
        relative_path:str = os.path.relpath(path=item_path, start=base_original)
        target_path:str = os.path.join(base_replica, relative_path)

        if os.path.isdir(item_path):
            if not os.path.exists(target_path):
                os.makedirs(target_path)
                logging.info(f"[CREATED] Folder: {target_path}")

        else:
            shutil.copy2(item_path, target_path)
            logging.info(f"[CREATED] File: {item_path} -> {target_path}")


    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures:List[concurrent.futures.Future] = []
        for root, dirs, files in os.walk(original_folder_path):
            for name in dirs + files:
                item_path:str = os.path.join(root, name)
                futures.append(executor.submit(copy_item, item_path, original_folder_path, replica_folder_path))
        
        concurrent.futures.wait(futures)        


def update_replica_folder(original_folder_path: str, replica_folder_path: str) -> None:

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures:List[concurrent.futures.Future] = []

        # Loop through the original folder and update the replica
        for root, dirs, files in os.walk(original_folder_path, topdown=True):
            for file in files:
                original_file:str = os.path.normpath(os.path.join(root, file))
                relative_file_path:str = os.path.normpath(os.path.relpath(path=original_file, start=original_folder_path))
                replica_file:str = os.path.normpath(os.path.join(replica_folder_path, relative_file_path))

                if not os.path.exists(replica_file):
                    futures.append(executor.submit(copy_file, original_file, os.path.join(replica_folder_path, relative_file_path)))

                elif (os.stat(original_file).st_mtime) > (os.stat(os.path.join(replica_folder_path, relative_file_path)).st_mtime):
                    futures.append(executor.submit(copy_file, original_file, replica_file))


            for dir in dirs:
                original_dir:str = os.path.normpath(os.path.join(root, dir))
                relative_path:str = os.path.normpath(os.path.relpath(path=original_dir, start=original_folder_path))
                replica_dir:str = os.path.normpath(os.path.join(replica_folder_path, relative_path))
                
                if not os.path.exists(replica_dir):
                    os.makedirs(replica_dir)
                    logging.info(f"Deleted folder: {replica_dir}")

                if os.stat(original_dir).st_mtime > os.stat(replica_dir).st_mtime:
                    futures.append(executor.submit(copy_file, original_dir, replica_dir))


                    
        # Search for files that do not match the original
        for root, dirs, files in os.walk(replica_folder_path, topdown=False):
            for name in files:
                replica_file:str = os.path.normpath(os.path.join(root, name))
                original_file:str = os.path.normpath(os.path.join(original_folder_path, os.path.relpath(path=replica_file, start=replica_folder_path)))

                if not os.path.exists(original_file):
                    futures.append(executor.submit(delete_extra_files, replica_file))

            for name in dirs:
                replica_dir:str = os.path.normpath(os.path.join(root, name))
                original_dir:str = os.path.normpath(os.path.join(original_folder_path, os.path.relpath(path=replica_dir, start=replica_folder_path)))

                if not os.path.exists(original_dir):
                    futures.append(executor.submit(delete_extra_files, replica_dir))

        concurrent.futures.wait(futures)



def synchronize(original_folder_path:str, replica_folder_path:str, changes:list):
    for change in changes:
        rel_path:str = os.path.relpath(change['path'], original_folder_path)
        dst_path:str = os.path.join(replica_folder_path, rel_path)
        print(changes)

        if change['type'] == 'created':

            if os.path.isfile(change['path']):
                copy_file(change['path'], dst_path)
                logging.info(f"[CREATED] File: {dst_path}")
            else:
                shutil.copytree(change['path'], dst_path)
                logging.info(f"[CREATED] Folder: {dst_path}")


        elif change['type'] == 'deleted':

            if os.path.isfile(change['path']):
                os.remove(dst_path)
                logging.info(f"[DELETED] File: {os.path.normpath(dst_path)}")
            else:
                shutil.rmtree(dst_path)
                logging.info(f"[DELETED] Folder: {os.path.normpath(dst_path)}")


        elif change['type'] == 'renamed':

            if change['is_file']:
                os.rename(dst_path, change['path'])
                logging.info(f"[RENAMED] File: {os.path.normpath(dst_path)} -> {os.path.normpath(change['path'])}")
            else:
                os.rename(dst_path, change['path'])
                logging.info(f"[RENAMED] Folder: {os.path.normpath(dst_path)} -> {os.path.normpath(change['path'])}")




if __name__ == "__main__":
    ...

