from ..utils.points import Point, cardinal_surrounding_points, pointstr, surrounding_points
from collections import deque

def parse_heights(test):
    test_str = '-test' if test else ''
    heights = {}
    with open(f'advent/2021/input_files/9{test_str}.txt') as f:
        for y, line in enumerate(f):
            line = line.strip()
            for x, height in enumerate(line):
                heights[Point(x, y)] = int(height)
    return heights

def find_low_points(heights):
    lows = []
    for point, height in heights.items():
        surrounding_heights = [heights.get(surrounding_point) for surrounding_point in cardinal_surrounding_points(point)]
        surrounding_heights = [surrounding_height for surrounding_height in surrounding_heights if surrounding_height is not None]
        all_greater = all(map(lambda h: h > height, surrounding_heights))
        if all_greater:
            lows.append(point)
    return lows

def part1(test):
    heights = parse_heights(test)
    lows = find_low_points()
    print(f'{len(lows)} lows found:')
    for point in lows:
        print(f'\t({pointstr(point)}): {heights[point]}')
    risk_level = sum([1 + heights[point] for point in lows])
    print(f'Risk level: {risk_level}')

def calculate_basin_size(low_point, heights):
    basin = set()
    stack = deque([low_point])
    while stack:
        current_point = stack.pop()
        if current_point in basin:
            continue
        basin.add(current_point)
        for surrounding_point in cardinal_surrounding_points(current_point):
            if heights.get(surrounding_point, 10) < 9:
                stack.append(surrounding_point)
    return len(basin)
    
def part2(test):
    heights = parse_heights(test)
    lows = find_low_points(heights)
    basin_sizes = []
    for low_point in lows:
        basin_size = calculate_basin_size(low_point, heights)
        print(f'Basin @ {pointstr(low_point)} -> {basin_size}')
        basin_sizes.append(basin_size)
    
    basin_sizes.sort()
    result = basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]
    print(result)
        
        
        
            
# part1(True)
# part1(False)

# part2(True)
part2(False)        
