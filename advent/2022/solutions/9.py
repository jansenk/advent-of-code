from advent.util import minmax
from advent.util.points import Direction, Point, move, unit_vector, vector, chebshayev_distance
from ..utils import iterlines        

def instructions(test_case=None):
    for line in iterlines(9, test_case=test_case):
        direction, magnitude = line.split()
        yield Direction.parse(direction), int(magnitude)

def is_inline(head, tail):
    return head.x == tail.x or head.y == tail.y

def move_tail(head, tail):
    d = chebshayev_distance(head, tail)
    if d <= 1:
        return tail
    v = vector(tail, head)
    uv = unit_vector(v)
    return move(tail, uv)

def print_rope(start, rope):
    map = {start: 's'}
    enumerated_rope = list(enumerate(rope))
    enumerated_rope.reverse()
    for i, p in enumerated_rope:
        map[p] = str(i)
    
    _print_map(start, rope, map)

def print_trail(start, trail):
    map = {p: '#' for p in trail}
    map[start] = 's'
    _print_map(start, trail, map)

def _print_map(start, points, map):
    min_x, max_x = minmax([p.x for p in points] + [start.x])
    min_y, max_y = minmax([p.y for p in points] + [start.y])

    for y in range(max_y+3, min_y-4, -1):
        line = []
        for x in range(min_x-3, max_x+4):
            line.append(map.get(Point(x, y), '.'))
        print("".join(line))

def simulate_rope(instr, rope_len, debug=False):
    start = Point(0, 0)
    rope = [start for _ in range(rope_len)]
    tail_points = {start}
    for direction, magnitude in instr:
        if debug:
            print(f"Moving {magnitude} spaces {Direction.name(direction)}")
        for _ in range(magnitude):
            rope[0] = move(rope[0], direction)
            for i in range(1, rope_len):
                rope[i] = move_tail(rope[i-1], rope[i])
            tail_points.add(rope[-1])
        if debug:
            print_rope(start, rope)
    print(len(tail_points))
    if debug:
        print_trail(start, tail_points)

def part1(test_case=None, debug=False):
    simulate_rope(
        instructions(test_case),
        2,
        debug
    )

def part2(test_case=None, debug=False):
    simulate_rope(
        instructions(test_case),
        10,
        debug
    )

part1(1)
part1()
part2(1)
part2(2)
part2()