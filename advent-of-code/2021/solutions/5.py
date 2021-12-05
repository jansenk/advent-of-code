import re
from ..utils.points import Point, move # I call this point, but I use it kinda interchangbly with the concept of vectors
from fractions import Fraction
from collections import Counter

line_re = r'(\d+),(\d+) -> (\d+),(\d+)'
def read_lines(filename):
    with open('advent-of-code/2021/input_files/' + filename) as f:
        input_lines = [line.strip() for line in f.readlines()]
    lines = []
    for input_line in input_lines:
        match = re.match(line_re, input_line)        
        assert match is not None
        x1, y1, x2, y2 = list(map(int, match.groups()))
        lines.append((Point(x1, y1), Point(x2, y2)))
    return lines

def is_horizontal(p1, p2):
    return p1.y == p2.y

def is_vertical(p1, p2):
    return p1.x == p2.x
    
def get_step(p1, p2):
    dx = p2.x - p1.x
    norm_dx = int(dx / abs(dx)) if dx != 0 else 0
    dy = p2.y - p1.y
    norm_dy = int(dy / abs(dy)) if dy != 0 else 0
    return Point(norm_dx,  norm_dy)
            
            
 # / LTR 
# / RTL
 # \ LTR
 # \ RTL   
 #
        
    # dx = p2.x - p1.x
    # dy = p2.y - p1.y
    # try:
    #     f = Fraction(dy, dx)
    #     return Point(f.denominator, f.numerator)
    # except ZeroDivisionError:
    #     return Point(dx, 0)

def points_along_line(p1, p2):
    s = get_step(p1, p2)
    current_point = p1
    while current_point != p2:
        yield current_point
        current_point = move(current_point, s)
    yield p2

def part1(lines):
    point_counter = Counter()
    for p1, p2 in lines:
        print(p1, p2)
        if not is_horizontal(p1, p2) and not is_vertical(p1, p2):
            print(f'Line ({p1.x}, {p1.y}) -> ({p2.x}, {p2.y}) is not horizontal or vertical')
            continue
        for point in points_along_line(p1, p2):
            print(point)
            point_counter.update([point])
    print(len([elem for elem, count in point_counter.items() if count > 1]))

def part2(lines):
    point_counter = Counter()
    for p1, p2 in lines:
        print(p1, p2)
        for point in points_along_line(p1, p2):
            print(point)
            point_counter.update([point])
    print(len([elem for elem, count in point_counter.items() if count > 1]))

# test_lines = read_lines('5-test.txt')
# # part1(test_lines)
# part2(test_lines)

lines = read_lines('5.txt')
# part1(lines)
part2(lines)

