import os
import hashlib
from typing_extensions import List


class Node:
    def __init__(self, name, path, is_file):
        self.name = name
        self.path = path
        self.is_file = is_file
        self.hash:str = ""
        self.children: List['Node'] = []

    def __str__(self, level=0) -> str:
        ret = "\t" * level + f"Node(name={self.name}, is_file={self.is_file}, hash={self.hash}, path={self.path})\n"

        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self) -> str:
        return f"Node(name={self.name}, path={self.path}, is_file={self.is_file}, hash={self.hash}, children={self.children})"



def calculate_hash(file_path:str) -> str:
    with open(file_path, "rb") as f:
        hash_file = hashlib.md5(f.read()).hexdigest()

    return hash_file


def build_tree(path:str) -> Node:
    normalized_path:str = os.path.normpath(path)
    is_file:bool = os.path.isfile(normalized_path)
    node:Node = Node(name=os.path.basename(normalized_path), path=normalized_path, is_file=is_file)

    if is_file:
        node.hash = calculate_hash(normalized_path)

    else:
        for item in os.listdir(normalized_path):
            child_path:str = os.path.join(normalized_path, item)
            node.children.append(build_tree(child_path))

    return node






if __name__ == "__main__":
    print(build_tree("D:/Root"))
