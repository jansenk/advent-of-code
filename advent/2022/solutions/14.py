from collections import namedtuple
from dataclasses import dataclass
from operator import is_
from unicodedata import name
from ..utils import iterlines, Window
from advent.util.points import Point, Direction, move, vector_to, unit_vector

def parse_cave(is_test):
    walls = set()
    window = Window()
    
    for line in iterlines(14, is_test):
        points_str = line.split(" -> ")
        points = []
        for point_str in points_str:
            tokens = point_str.split(",")
            x, y = int(tokens[0]), int(tokens[1])
            p = Point(x, y)
            points.append(p)
            window.extend(p)
    
        for i in range(len(points) - 1):
            point = points[i]
            next_point = points[i+1]
            v = vector_to(point, next_point)
            uv = unit_vector(v)
            current_point = point
            while current_point != next_point:
                walls.add(current_point)
                current_point = move(current_point, uv)
            walls.add(next_point)
    return window, walls

def print_state(window, walls, sand, has_floor=False):
    y_inc = 1 if not has_floor else 3
    for y in range(window.y_range.rmax + y_inc):
        row = []
        x_range = range(
            window.x_range.rmin,
            window.x_range.rmax + 1,
        )
        for x in x_range:
            p = Point(x, y)
            char = "."
            if p in walls:
                char = '#'
            elif has_floor and y == window.y_range.rmax + 2:
                char = '#'
            elif p in sand:
                char = 'o'
            row.append(char)
        print("".join(row))
    print("\n")

SAND_SPAWN = Point(500, 0)

def fill_sand(window, walls, has_floor=False):
    sand = set()
    while (next_sand_resting_position := single_sand(window, walls, sand, has_floor)) is not None:
        sand.add(next_sand_resting_position)
        # print_state(window, walls, sand, has_floor)
        if has_floor:
            window.x_range.extend(next_sand_resting_position.x)
            if next_sand_resting_position == SAND_SPAWN:
                break
    return window, walls, sand

def despawn_single_sand(window, p, has_floor):
    if has_floor:
        return False
    return p.y <= window.y_range.rmax
    
def single_sand(window, walls, sand, has_floor):
    current_point = SAND_SPAWN
    while not despawn_single_sand(window, current_point, has_floor):
        next_p = next_sand_move(window, walls, sand, current_point, has_floor)
        if next_p is None:
            return current_point
        else:
            current_point = next_p
    return None

def next_sand_move(window, walls, sand, p, has_floor):
    for d in [Direction.UP, Direction.UL, Direction.UR]:
        next_p = move(p, d)
        if not blocked(window, walls, sand, next_p, has_floor):
            return next_p
    return None

def blocked(window, walls, sand, p, has_floor):
    if p in walls or p in sand:
        return True
    elif has_floor and p.y == window.y_range.rmax + 2:
        return True
    else:
        return False


def part1(is_test):
    window, walls = parse_cave(is_test)
    print_state(window, walls, set())    
    window, walls, sand = fill_sand(window, walls)
    print_state(window, walls, sand)
    print(len(sand))

# part1(False)

def part2(is_test):
    window, walls = parse_cave(is_test)
    print_state(window, walls, set())
    window, walls, sand = fill_sand(window, walls, True)
    print_state(window, walls, sand)
    print(len(sand))

part2(False)