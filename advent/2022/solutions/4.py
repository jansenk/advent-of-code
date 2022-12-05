from ..utils import iterlines
from collections import namedtuple

ElfRange = namedtuple('ElfRange', ['min', 'max'])

def parse(is_test):
    ranges = []
    for line in iterlines(4, is_test):
        elf1, elf2 = line.split(",")
        elf1range = ElfRange(*tuple(map(int, elf1.split("-"))))
        elf2range = ElfRange(*tuple(map(int, elf2.split("-"))))
        ranges.append((elf1range, elf2range))
    return ranges

test_ranges = parse(True)
ranges = parse(False)

def contains(bigger, smaller):
    return bigger.min <= smaller.min and bigger.max >= smaller.max
     
def part1(ranges):
    result = 0
    for range1, range2 in ranges:
        if contains(range1, range2) or contains(range2, range1):
            result += 1
    print(result)

part1(test_ranges)
part1(ranges)

def contains_point(range, p):
    return range.min <= p and p <= range.max
def overlaps(r1, r2):
    return any([
        contains_point(r1, r2.min),
        contains_point(r1, r2.max),
        contains_point(r2, r1.min),
        contains_point(r2, r1.max)
    ])

def part2(ranges):
    result = 0
    for r1, r2 in ranges:
        if overlaps(r1, r2):
            result += 1
    print(result)

part2(test_ranges)
part2(ranges)    
        
        