from ..utils.points import Point, surrounding_points

def parse_squids(test):
    test_str = '-test' if test else ''
    with open(f'advent/2021/input_files/11{test_str}.txt') as f:
        squidmap = {}
        for y, line in enumerate(f):
            for x, c in enumerate(line.strip()):
                squidmap[Point(x, y)] = int(c)
    return squidmap

def tick_squid(p, squidmap):
    if p in squidmap:
        squidmap[p] += 1
        if squidmap[p] > 9:
            return True
    return False

def increase_all_squids_by_1(squidmap):
    flashes = []
    for point in squidmap:
        if tick_squid(point, squidmap):
            flashes.append(point)
    return flashes

from collections import deque
def squidtick(squidmap):
    completed_flashes = set()
    flash_queue = deque()
    
    initial_flashes = increase_all_squids_by_1(squidmap)
    flash_queue.extend(initial_flashes)
    
    while flash_queue:
        current_flash = flash_queue.pop()
        if current_flash in completed_flashes:
            continue
        completed_flashes.add(current_flash)

        for surrounding_point in surrounding_points(current_flash):
            if surrounding_point not in squidmap or surrounding_point in completed_flashes:
                continue
            if tick_squid(surrounding_point, squidmap):
                flash_queue.appendleft(surrounding_point)
    
    for flash in completed_flashes:
        squidmap[flash] = 0
    
    return completed_flashes


from blessings import Terminal
def print_squids(squidmap, flashes, term=None):
    if term is None:
        term = Terminal()
    for y in range(10):
        line = ""
        for x in range(10):
            p = Point(x, y)
            value = str(squidmap[p])
            if p in flashes:
                line += term.bold + value + term.normal 
            else:
                line += value
        print(line)
    print()

def test_printsquids():
    squidmap = parse_squids(True)
    print_squids(squidmap, set())
    print('\n\n')
    print_squids(
        squidmap,
        set([
            Point(0, 0),
            Point(1, 0),
            Point(0, 1),
            Point(1, 1),
            Point(9, 9),
        ])
    )

def part1(squidmap):
    print("Before Any Steps:")
    print_squids(squidmap, set())
    
    total_flashes = 0
    for step in range(1, 101):
        flashes = squidtick(squidmap)
        total_flashes += len(flashes)
        if step <= 10 or step % 10 == 0:
            print(f"After step {step}:")
            print_squids(squidmap, flashes)
        print(f"After 100 steps, there have been {total_flashes} flashes")
        
def part2(squidmap):
    step = 0
    while True:
        step += 1
        print(f"Step {step}")
        flashes = squidtick(squidmap)
        print_squids(squidmap, flashes)
        if len(flashes) == 100:
            print(f"Synchronized at step {step}")
            return
        
    
import time
def pretty_squids(squidmap):
    term = Terminal()
    try:
        while True:
            flashes = squidtick(squidmap)
            print(term.clear)
            print_squids(squidmap, flashes, term=term)
            time.sleep(0.3)
    except KeyboardInterrupt:
        print(term.clear)
        return

        
if __name__ == "__main__":
    # test_squids = parse_squids(True)
    # part1(test_squids)
    
    squids = parse_squids(False)
    pretty_squids(squids)
