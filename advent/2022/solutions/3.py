from ..utils import iterlines

def parse_inputs(is_test):
    lines = []
    for line in iterlines(3, is_test):
        half_i = int(len(line) / 2)
        left_half = line[:half_i]
        right_half = line[half_i:]
        lines.append((left_half, right_half))
    return lines

test_lines = parse_inputs(True)
lines = parse_inputs(False)

PRIORITIES = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def priority(c):
    return PRIORITIES.index(c)
    
def part1(lines):
    total = 0
    for left, right in lines:
        common = set(left).intersection(set(right))
        assert len(common) == 1
        common = common.pop()
        assert len(common) == 1
        total += priority(common)
    print(total)
    
part1(test_lines)
part1(lines)

def groups(lines):
    i = 0
    while i < len(lines):
        yield lines[i:i+3]
        i += 3

def part2(lines):
    total = 0
    for e1, e2, e3 in groups(lines):
        e1_set = set(e1[0] + e1[1])
        e2_set = set(e2[0] + e2[1])
        e3_set = set(e3[0] + e3[1])
        common = e1_set.intersection(e2_set).intersection(e3_set)
        total += priority(common.pop())
    print(total)

part2(test_lines)
part2(lines)

