from collections import namedtuple
from curses import window
from itertools import combinations

from advent.util.points import Direction, Point, manhattan_distance, move
from ..utils import iterlines, Window, Range
from re import match

Zone = namedtuple("Zone", ["sensor", "beacon", "distance"])

INPUT_PATTERN = r"Sensor at x=(?P<sx>(-?\d+)), y=(?P<sy>(-?\d+)): closest beacon is at x=(?P<bx>(-?\d+)), y=(?P<by>(-?\d+))"
def parse(is_test):
    window = Window()
    zones = []
    for line in iterlines(15, is_test):
        m = match(INPUT_PATTERN, line)
        assert m
        sensor = Point(
            int(m['sx']),
            int(m['sy']),
        )
        beacon = Point(
            int(m['bx']),
            int(m['by']),
        )
        distance = manhattan_distance(sensor, beacon)
        zone = Zone(
            sensor,
            beacon,
            distance
        )
        extend_window(zone, window)
        zones.append(zone)

    return window, zones

def find_y_intersection(zone, target_y):        
    top_down = Range()
    top_down.extend(zone.sensor.y + zone.distance)
    top_down.extend(zone.sensor.y - zone.distance)
    if target_y in top_down:
        distance_from_center = abs(zone.sensor.y - target_y)
        radius = zone.distance - distance_from_center
        intersection = Range(
            zone.sensor.x - radius,
            zone.sensor.x + radius,
        )
        return intersection
    else:
        return None
        

def extend_window(zone:Zone, window:Window):
    window.extend(zone.sensor)
    window.extend(zone.beacon)
    for d in Direction.CARDINAL:
        window.extend(move(zone.sensor, d.scale(zone.distance)))

def print_zones(zones):
    print("[")
    for zone in zones:
        print(f"S{zone.sensor} B{zone.beacon}")
    print("]")

def find_intersections(zones, target_y):
    # print_zones(zones)
    y_intersections = []
    for zone in zones:
        intersection = find_y_intersection(zone, target_y)
        if intersection is not None:
            y_intersections.append(intersection)
    all_resolved = False
    while not all_resolved:
        next_round = []
        for intersection in y_intersections:
            squished = False
            for i in range(len(next_round)):
                nr = next_round[i]
                if nr.overlaps(intersection) or intersection.overlaps(nr):
                    squished = True
                    next_round[i] = nr.combine(intersection)
            if not squished:
                next_round.append(intersection)                    
        if len(next_round) == len(y_intersections):
            all_resolved = True
        else:
            y_intersections = next_round
    intersecting_points = set()
    for zone in zones:
        for point in [zone.sensor, zone.beacon]:
            if check_if_point_in(y_intersections, target_y, point):
                intersecting_points.add(point)
    lens = [len(i) for i in y_intersections]
    total_len = sum(lens)
    return y_intersections, intersecting_points

def check_if_point_in(intersections, target_y, p):
    if p.y == target_y:
        for intersection in intersections:
            if p.x in intersection:
                return True
    return False

def part1(is_test, y_intersect):
    window, zones = parse(is_test)
    intersections, intersecting_points = find_intersections(zones, y_intersect)
    lens = [len(i) for i in intersections]
    total_len = sum(lens)
    print(total_len - len(intersecting_points))

part1(True, 10)
part1(False, 2_000_000)

# This solution is bad and takes like, over a minute, but I don't care lmao
def part2(is_test, bound):
    window, zones = parse(is_test)
    y_iter = iter(bound)
    for y in y_iter:
        if y % 100_000 == 0:
            print(y)
        intersections, intersecting_points = find_intersections(zones, y)
        intersections = [intersection.limit(bound) for intersection in intersections]
        if len(intersections) > 1:
            print(y)
            print(", ".join([str(i) for i in intersections]))


part2(False, Range(0, 4_000_000))