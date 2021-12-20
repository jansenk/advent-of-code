from ..utils.points import Point, move

TARGET = {'x': (85, 145), 'y': (163, -108)}
TEST_TARGET = {'x': (20, 30), 'y': (-10, -5)}

def between(x, a, b):
    return (a <= x <= b) or (b <= x <= a)

class Target:
    def __init__(self, close_side_x, far_side_x, bottom, top):
        self.close_side_x = close_side_x
        self.far_side_x = far_side_x
        self.top = top
        self.bottom = bottom
    
    def __contains__(self, point):
        return between(point.x, self.close_side_x, self.far_side_x) and between(point.y, self.top, self.bottom)
    
    def has_been_overshot(self, point):
        return point.x > self.far_side_x or point.y < self.bottom


TARGET = Target(85, 145, -163, -108)
TEST_TARGET = Target(20, 30, -10, -5)


def get_next_velocity(current):
    if current.x > 0:
        next_x = current.x - 1
    elif current.x < 0:
        next_x = current + 1
    else:
        next_x = 0
    
    return Point(next_x, current.y -1)

def arc_generator(starting_velocity):
    current_point = starting_velocity
    current_velocity = starting_velocity
    while True:
        yield current_point
        current_velocity = get_next_velocity(current_velocity)
        current_point = move(current_point, current_velocity)

def sumn(n):
    return int((n * (n + 1)) / 2)

from math import sqrt
def find_min_x_velocity(target_x_min):
    rough_n = int(sqrt(target_x_min * 2))
    for n in (rough_n - 1, rough_n, rough_n + 1):
        x = sumn(n)
        if x >= target_x_min:
            return n
    
def find_x_range(target):
    min_x = find_min_x_velocity(target.close_side_x)
    max_x = target.far_side_x
    return min_x, max_x
    
def get_projectile_line(velocity, target):
    point_gen = arc_generator(velocity)
    current_point = next(point_gen)
    line = [current_point]
    while not target.has_been_overshot(current_point):
        if current_point in target:
            return True, line
        current_point = next(point_gen)
        line.append(current_point)
    return False, line

def get_line_boundaries(line, target):
    min_x = 0
    max_x = target.far_side_x
    min_y = target.bottom
    max_y = max(target.top, 0)
    for point in line:
        if point.x < min_x:
            min_x = point.x
        if point.x > max_x:
            max_x = point.x
        if point.y < min_y:
            min_y = point.y
        if point.y > max_y:
            max_y = point.y
    return min_x, min_y, max_x, max_y

def draw_line(line, target):
    min_x, min_y, max_x, max_y = get_line_boundaries(line, target)
    for y in range(max_y, min_y - 1, -1):
        row = []
        for x in range(min_x, max_x + 1):
            point = Point(x, y)
            icon = '.'
            if point in target:
                icon = 'T'
            if point in line:
                icon = '#'
            if (x, y) == (0, 0):
                icon = 'S'
            row.append(icon)
        print(''.join(row))
    print('\n')

def highpoint(line):
    return max([point.y for point in line])

def find_hits(target):
    min_x_velocity, max_x_velocity = find_x_range(target)
    min_y_velocity, max_y_velocity = target.bottom, abs(target.bottom)
    hits = []
    for x_velocity in range(min_x_velocity, max_x_velocity + 1):
        for y_velocity in range(min_y_velocity, max_y_velocity):
            velocity = Point(x_velocity, y_velocity)
            in_target, line = get_projectile_line(velocity, target)
            if not in_target:
                continue
            else:
                hits.append((velocity, line))
    return hits

def find_highest(hits):
    highpoints = [highpoint(line) for _, line in hits]
    return max(highpoints)

def solve(target):
    hits = find_hits(target)
    highest = find_highest(hits)
    print(f'Part 1: {highest}')
    print(f'Part 2: {len(hits)}')

def fire_and_print(velocity, target):
    _, line = get_projectile_line(velocity, target)
    draw_line(line, target)
    print(f"High: {highpoint(line)}")

if __name__ == '__main__':
    # for x in range(6, 10):
    #     for y in range(5, 50):
    #         breakpoint()
    #         print(x, y)
    #         fire_and_print(Point(x, y), TEST_TARGET)
    # fire_and_print(Point(7, 2), TEST_TARGET)
    # fire_and_print(Point(6, 3), TEST_TARGET)
    # fire_and_print(Point(5, 3), TEST_TARGET)
    # fire_and_print(Point(4, 3), TEST_TARGET)
    # fire_and_print(Point(9, 0), TEST_TARGET)
    # fire_and_print(Point(17, -4), TEST_TARGET)

    solve(TEST_TARGET)
    solve(TARGET)
