from ..utils import iterlines
from typing import Dict, List, Optional, Tuple

class Node:
    def __init__(self, name: str, parent: Optional["Node"]) -> "Node":
        self.name: str = name
        self.parent: Optional[Node] = parent

class Dir(Node):
    def __init__(self, name: str, parent: Optional["Dir"]) -> Node:
        super().__init__(name, parent)
        self.children: Dict[str, Node] = {}
        self.size = None

    def calculate_filesize(self):
        assert self.parent == None
        self.filesize()

    def all_subdirectories(self):
        result = []
        for child in self.children.values():
            if isinstance(child, Dir):
                result.append(child)
                result.extend(child.all_subdirectories())
        return result

    def filesize(self) -> int:
        if self.size == None:
            self.size = sum([child.filesize() for child in self.children.values()])
        return self.size
    
    def mkdir(self, name) -> None:
        self.children[name] = Dir(name, self)
    
    def touch(self, name, size) -> None:
        self.children[name] = File(name, self, size)
        
    def cd(self, name) -> "Dir":
        if name == "..":
            return self.parent
        else:
            target: Dir = self.children[name]
            assert isinstance(target, Dir)
            return target
    
    def __getitem__(self, name):
        return self.children[name]
        
class File(Node):
    def __init__(self, name: str, parent: Dir, size: int) -> "File":
        super().__init__(name, parent)
        self.size: int = size
        
    def filesize(self) -> int:
        return self.size

def parse_ls(commands: List[List[str]], current_directory: Dir, ip: int) -> int:
    ip += 1 # look at the line after ls where the files start
    while ip < len(commands) and (line := commands[ip])[0] != "$":
        descriptor, name = line
        if descriptor == "dir":
            current_directory.mkdir(name)
        else:
            assert descriptor.isdigit()
            current_directory.touch(name, int(descriptor))
        ip += 1
    return ip
    
def perform_command(commands:List[List[str]], current_directory:Dir, ip:int) -> Tuple[int, Dir]:
    line:List[str] = commands[ip]
    assert line[0] == "$"
    command:str = line[1]
    if command == "ls":
        return parse_ls(commands, current_directory, ip), current_directory
    elif command == "cd":
        return ip + 1, current_directory.cd(line[2])

        
def parse_directory_structure(is_test: bool) -> Dir:
    commands: List[List[str]] = [line.split() for line in iterlines(7, is_test)]
    ip:int = 1
    root:Dir = Dir("", None)
    current_directory:Dir = root
    while ip < len(commands):
        line:List[str] = commands[ip]
        if line[0] == "$":
            ip, current_directory = perform_command(commands, current_directory, ip)
    return root

test_root:Dir = parse_directory_structure(True)
root:Dir = parse_directory_structure(False)

test_root.calculate_filesize()
root.calculate_filesize()

test_subdirectories = test_root.all_subdirectories()
subdirectories = root.all_subdirectories()

def part1(subdirectories:List[Dir]) -> None:
    total = 0
    for directory in subdirectories:
        if directory.size <= 100_000:
            total += directory.size
    print(total)

part1(test_subdirectories)            
part1(subdirectories)

def part2(root:Dir, subdirectories:List[Dir]) -> None:
    total_space = 70_000_000
    space_needed_for_update = 30_000_000
    current_used_space = root.size
    current_free_space = total_space - current_used_space
    free_space_needed_to_clean = space_needed_for_update - current_free_space
    
    print(f"used={current_used_space}")
    print(f"free={current_free_space}")
    print(f"needed={free_space_needed_to_clean}")
    
    big_enough = [d.size for d in subdirectories if d.size >= free_space_needed_to_clean]
    print(min(big_enough))
    
part2(test_root, test_subdirectories)
part2(root, subdirectories)


    