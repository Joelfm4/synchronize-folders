import os
from typing_extensions import List

original_absulute_path:str = ""

class Node:
    def __init__(self, name, path, relative_path,is_file):
        self.name = name
        self.path = path
        self.relative_path = relative_path
        self.is_file = is_file
        self.children: List['Node'] = []


    def __str__(self, level=0) -> str:
        ret = "\t" * level + f"Node(name={self.name}, is_file={self.is_file}, path={self.path}), relative_path={self.relative_path}\n"

        for child in self.children:
            ret += child.__str__(level + 1)
        return ret


    def __repr__(self) -> str:
        return f"Node(name={self.name}, path={self.path}, is_file={self.is_file}, children={self.children})"


def build_tree(path:str) -> Node:
    normalized_path:str = os.path.normpath(path)
    is_file:bool = os.path.isfile(normalized_path)
    relative_path:str = os.path.relpath(normalized_path, original_absulute_path)
    node:Node = Node(name=os.path.basename(normalized_path), path=normalized_path, relative_path=relative_path,is_file=is_file)

    if not is_file:
        for item in os.listdir(normalized_path):
            child_path:str = os.path.join(normalized_path, item)
            node.children.append(build_tree(child_path))

    return node


if __name__ == "__main__":
    print(build_tree("D:/Root"))
