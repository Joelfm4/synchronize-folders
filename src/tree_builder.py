import os
import hashlib
from typing_extensions import Optional, List
from datetime import datetime


class Node:
    def __init__(self, name, path, is_file, timestamp):
        self.name = name
        self.path = path
        self.is_file = is_file
        self.hash: Optional[str] = None 
        self.children: List['Node'] = []
        self.timestamp = timestamp

    def __str__(self, level=0) -> str:
        ret = "\t" * level + f"Node(name={self.name}, is_file={self.is_file}, hash={self.hash}, path={self.path}, timestamp={self.timestamp})\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self) -> str:
        return f"Node(name={self.name}, path={self.path}, is_file={self.is_file}, hash={self.hash})"



def calculate_hash(file_path:str) -> str:
    with open(file_path, "rb") as f:
        hash_file = hashlib.md5(f.read()).hexdigest()

    return hash_file


def build_tree(path:str) -> Node:
    path:str = os.path.normpath(path)
    is_file:bool = os.path.isfile(path)
    node:Node = Node(name=os.path.basename(path), path=path, is_file=is_file, timestamp=datetime.now())

    if is_file:
        node.hash = calculate_hash(path)

    else:
        for item in os.listdir(path):
            child_path:str = os.path.join(path, item)
            node.children.append(build_tree(child_path))

    return node



def main(path:str) -> None:
    return build_tree(path) 



if __name__ == "__main__":
    print(main("D:/Root"))
