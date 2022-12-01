from collections import namedtuple
from ..utils.points import Point3D
from math import prod

Range = namedtuple('Range', ['min', 'max'])
class Cube:
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax, is_active=True):
        self.x = Range(xmin, xmax)
        self.y = Range(ymin, ymax)
        self.z = Range(zmin, zmax)
        self.is_active = True
        
    @staticmethod
    def do_cubes_intersect(a, b):
        return all([
            (a.x.min <= b.x.max and a.x.max >= b.x.min),
            (a.y.min <= b.y.max and a.y.max >= b.y.min),
            (a.z.min <= b.z.max and a.z.max >= b.z.min),
        ])

    def encompasses(self, other):
        return all([
            (self.x.min <= other.x.min <= self.x.max),
            (self.x.min <= other.x.max <= self.x.max),
            (self.y.min <= other.y.min <= self.y.max),
            (self.y.min <= other.y.max <= self.y.max),
            (self.z.min <= other.z.min <= self.z.max),
            (self.z.min <= other.z.max <= self.z.max),        
        ])

    @staticmethod
    def get_cube_intersection(a, b):
        x_intersect = b.x.max - a.x.min, a.x.max - b.x.min
        y_intersect = b.y.max - a.y.min, a.y.max - b.y.min
        z_intersect = b.z.max - a.z.min, a.z.max - b.z.min
        return Cube(*x_intersect, *y_intersect, *z_intersect)
    
    def area(self):
        return prod([
            abs(self.x.max - self.x.min + 1),
            abs(self.y.max - self.y.min + 1),
            abs(self.z.max - self.z.min + 1),
        ])

def parse_cubes(test=None):
    if test is not None:
        test_str = f'-test{test}'
    else:
        test_str = ''
    cubes = []
    parse_range_limits = lambda r: list(map(int, r[2:].split('..')))
    with open(f'advent/2021/input_files/22{test_str}.txt') as f:
        for line in f:
            onoff, ranges = line.strip().split()
            xrange_s, yrange_s, zrange_s = ranges.split(',')
            xrange = parse_range_limits(xrange_s)
            yrange = parse_range_limits(yrange_s)
            zrange = parse_range_limits(zrange_s)
            cubes.append(Cube(*xrange, *yrange, *zrange, is_active=onoff=='on'))
    return cubes

PART_1_BOUNDING_CUBE = Cube(-50, 50, -50, 50, -50, 50)
def bound_cube(cube):
    if not Cube.do_cubes_intersect(PART_1_BOUNDING_CUBE, cube):
        return None
    return PART_1_BOUNDING_CUBE.get_cube_intersection(cube)

def perform_reset(cubes, bound=True, debug=False):
    reactor = set()
    for i, cube in enumerate(cubes):
        if bound:
            cube  = bound_cube(cube)
            if cube is None:
                continue
        
        print(f'{i}: {len(instruction_set)} {instruction.onoff}')
        if instruction.onoff == ON:
            reactor.update(instruction_set)
        else:
            reactor.difference_update(instruction_set)
    return len(reactor)

def test_part_1():
    for test, expected_result in [(1, 39), (2, 590784), (3, 474140)]:
        instructions = parse_input(test)
        l = perform_reset(instructions)
        assert l == expected_result
        print(f"> Test {test} passes")
    print("> Part 1 tests pass")

def test_part_2():
    instructions = parse_input(3)
    l = perform_reset(instructions, bound=False, debug=True)
    assert l == 2758514936282235

if __name__ == '__main__':
    test_part_1()
    test_part_2()
    instructions = parse_input()
    print('--- Part 1 ---')
    print(perform_reset(instructions))
    print('--- Part 2 ---')
