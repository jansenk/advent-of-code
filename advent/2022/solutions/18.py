from collections import deque
from dataclasses import dataclass
from inspect import stack
from advent.util.points import Point3D, Vector3D, surrounding_3d_points
from ..utils import iterlines, Range, Window

@dataclass
class Zone(Window):
    def __init__(self):
        self.z_range = Range()
    
    def push(self, v):
        super().push(v)
        self.z_range.push(v)

    def extend(self, p3):
        super().extend(p3)
        self.z_range.extend(p3.z)
    
    def __contains__(self, p3):
        if not super().__contains__(p3):
            return False
        return p3.z in self.z_range

def parse_input(is_test):
    points = set()
    zone = Zone()
    for line in iterlines(18, is_test):
        coords = tuple(map(int, line.split(",")))
        p = Point3D(*coords)
        points.add(p)
        zone.extend(p)
    return points, zone

def surface_area(points, outside=None):
    sa = 0
    for point in points:
        for next_point in surrounding_3d_points(point):
            if not next_point in points:
                if outside is None or next_point in outside:
                    sa += 1
    return sa
                    
def make_steam(zone, points):
    seen = set()
    touching = set()
    zone.push(1)
    q = deque([
        Point3D(
            zone.x_range.rmin,
            zone.y_range.rmin,
            zone.z_range.rmin,
        )
    ])
    while q:
        current_point = q.pop()
        for next_point in surrounding_3d_points(current_point):
            if next_point not in zone:
                continue
            if next_point in seen:
                continue
            if next_point in points:
                touching.add(current_point)
                continue
            q.append(next_point)
        seen.add(current_point)
    return touching

            
    
    

def part1(is_test):
    points, _ = parse_input(is_test)
    sa = surface_area(points)
    print(sa)


def part2(is_test):
    points, zone = parse_input(is_test)
    steam = make_steam(zone, points)
    sa = surface_area(points, steam)
    print(sa)
    

part1(True)
part1(False)
part2(True)
part2(False)