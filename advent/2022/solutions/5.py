from dis import Instruction
import re
from collections import namedtuple

class CargoStack:
    def __init__(self, stacks_count):
        self.stacks_count = stacks_count
        self.stacks = [list() for _ in range(stacks_count)]

    def stack(self, i):
        return self.stacks[i-1]

    def put(self, i, s):
        self.stack(i).append(s)
    
    def pop(self, i):
        return self.stack(i).pop()
    
    def pop_chunk(self, i, n):
        stack = self.stacks[i-1]
        stack_l = len(stack)
        chunk_i = stack_l - n
        chunk = stack[chunk_i:]
        self.stacks[i-1] = stack[:chunk_i]
        return chunk
    
    def put_chunk(self, i, chunk):
        self.stack(i).extend(chunk) 
        
    def perform(self, instruction):
        print(instruction)
        for _ in range(instruction.count):
            item = self.pop(instruction.origin)
            self.put(instruction.dest, item)
    
    def perform_2(self, instruction):
        print(instruction)
        chunk = self.pop_chunk(instruction.origin, instruction.count)
        self.put_chunk(instruction.dest, chunk)
        
    def _safe_get(self, stack, i):
        try:
            return stack[i]
        except IndexError:
            return None
    
    def print(self):
        stacks = []
        max_stack_size = max(map(len, self.stacks))
        for i in range(max_stack_size):
            stacks.append([self._safe_get(stack, i) for stack in self.stacks])
        stacks.reverse()
        
        header = " "
        labels = list(range(1, len(self.stacks) + 1))
        header += "   ".join(map(str, labels))
        
        for stack_line in stacks:
            buf = ""
            for item in stack_line:
                if item is None:
                    buf += "    "
                else:
                    buf += f"[{item}] "
            print(buf)
        
        print(header)

def parse_stack_item_input(line):
    i = 0
    while i < len(line):
        item = line[i:i+3]
        if item[0] == '[' and item[2] == ']':
            yield item[1]
        else:
            yield None
        i += 4

def parse_cargo_stack(stacks_count, stacks):
    cargostack = CargoStack(stacks_count)
    for line in stacks:
        for i, item in enumerate(parse_stack_item_input(line)):
            if item is not None:
                cargostack.stacks[i].append(item)
    return cargostack

CraneInstruction = namedtuple("CraneInstruction", ['count', 'origin', 'dest'])
INSTRUCTION_PATTERN = r"move (?P<count>\d+) from (?P<origin>\d+) to (?P<dest>\d+)"

def parse_cargo(f):
        reading_stacks = True
        cargo = None
        stacks = []
        while reading_stacks:
            line = f.readline()
            line_chars = line.split()
            if all([len(c) == 1 and c.isdigit() for c in line_chars]):
                stacks.reverse()
                cargo = parse_cargo_stack(len(line_chars), stacks)
                reading_stacks = False
            else:
                stacks.append(line)
        cargo.print()
        return cargo

def parse_instructions(f):
    instructions = []
    for line in f.readlines():
        match = re.match(INSTRUCTION_PATTERN, line)
        assert match
        instructions.append(
            CraneInstruction(
                int(match['count']),
                int(match['origin']),
                int(match['dest'])
            )
        )
    return instructions

def parse(is_test):
    test_filename = "-test" if is_test else ""
    with open(f"advent/2022/input_files/5{test_filename}.txt") as f:
        cargo = parse_cargo(f)
        f.readline()
        instructions = parse_instructions(f)
        return cargo, instructions


def solve(cargostacks, instructions, part):
    for instr in instructions:
        if part == 1:
            cargostacks.perform(instr)
        else:
            cargostacks.perform_2(instr)
        cargostacks.print()


    result = ''
    for stack in cargostacks.stacks:
        result += stack.pop()
    print(result)

# test_stuff = parse(True)
# solve(*test_stuff, 2)

stuff = parse(False)
solve(*stuff, 2)
