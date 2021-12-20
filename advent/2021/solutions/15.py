from ..utils.points import Point

def parse_input(test):
    cave_map = dict()
    test_str = f'-test' if test else ''
    with open(f'advent/2021/input_files/15{test_str}.txt') as f:
        for y, line in enumerate(f):
            for x, danger in enumerate(line):
                cave_map[Point(x, y)] = int(danger)
    return cave_map, Point(x, y)

start = Point(0, 0)

def find_cheapest_path(cave_map, end):
    
    cheapest_path_from_start_to_node = dict()

    considered_points = set()
    
    
    
        
