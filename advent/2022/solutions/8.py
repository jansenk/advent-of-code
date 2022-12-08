from ast import parse
from collections import namedtuple
from dataclasses import dataclass
from re import L

from advent.util import points
from ..utils import iterlines
from typing import Dict
from advent.util.points import Point, move

@dataclass
class Forest:
    trees: Dict[Point, int]
    max_y: int
    max_x: int
    
    def corner(self, zero_x, zero_y):
        return Point(
            0 if zero_x else self.max_x,
            0 if zero_y else self.max_y
        )
    @property
    def topleft(self):
        return self.corner(True, True)
    
    @property
    def topright(self):
        return self.corner(False, True)
    
    @property
    def botleft(self):
        return self.corner(True, False)
    
    @property
    def botright(self):
        return self.corner(False, False)
    
    def __getitem__(self, item):
        assert isinstance(item, Point)
        return self.trees[item]

    def __contains__(self, item):
        return item in self.trees
    
    def print(self):
        for y in range(self.max_y + 1):
            line = [str(self[Point(x, y)]) for x in range(self.max_x +1)]
            print("".join(line))

def parse_forest(is_test):
    trees = {}
    for y, line in enumerate(iterlines(8, is_test)):
        for x, height in enumerate(line):
            p = Point(x, y)
            trees[p] = int(height)
    return Forest(trees, y, x)

test_forest = parse_forest(True)
forest = parse_forest(False)

def scan(
    forest,
    start,
    next_section_vector,
    next_point_vector,
    ):
    current_section_start_point = start
    result = set()
    while current_section_start_point in forest:
        section_visible = scan_section(forest, current_section_start_point, next_point_vector)
        result.update(section_visible)
        current_section_start_point = move(current_section_start_point, next_section_vector)
    return result


def scan_section(forest, starting_point, next_point_vector):
    # scans a row / column in some direction and returns set of visible trees
    current_point = starting_point
    result = set()
    current_visible_height = float("-inf")
    while current_point in forest:
        current_tree = forest[current_point]
        if current_tree > current_visible_height:
            result.add(current_point)
            current_visible_height = current_tree
        current_point = move(current_point, next_point_vector)
    return result

UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)

def brute_scan(forest):
    result = set()
    #Scan across the top row looking down
    result.update(scan(
        forest,
        forest.topleft,
        RIGHT,
        DOWN
    ))
    #Scan across the bottom row looking up
    result.update(scan(
        forest,
        forest.botleft,
        RIGHT,
        UP
    ))
    #Scan down the left side looking right
    result.update(scan(
        forest,
        forest.topleft,
        DOWN,
        RIGHT
    ))
    #Scan down the right side looking left
    result.update(scan(
        forest,
        forest.topright,
        DOWN,
        LEFT
    ))
    return result

def part1(forest):
    scan_results = brute_scan(forest)
    print(len(scan_results))

part1(test_forest)
part1(forest)

def part_2_subscan(forest, point, direction):
    current_distance = 0
    start_height = forest[point]
    current_point = move(point, direction)
    while current_point in forest:
        current_distance += 1
        if forest[current_point] >= start_height:
            return current_distance
        current_point = move(current_point, direction)
    return current_distance

def part_2_scan(forest, point):
    scenic_score = 1
    for direction in [UP, DOWN, LEFT, RIGHT]:
        score = part_2_subscan(forest, point, direction)
        scenic_score *= score
    return scenic_score

def part2(forest):
    scenic_scores = [part_2_scan(forest, point) for point in forest.trees]
    max_scenic = max(scenic_scores)
    print(max_scenic)

part2(test_forest)
part2(forest)