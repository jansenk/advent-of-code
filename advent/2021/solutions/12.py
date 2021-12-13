from collections import defaultdict

def parse_cave(test_num):
    cave_map = defaultdict(set)
    test_str = f'-{test_num}' if test_num is not None else ''
    with open(f'advent/2021/input_files/12{test_str}.txt') as f:
        for line in f:
            cave1, cave2 = line.strip().split('-')
            if cave2 != 'start':
                cave_map[cave1].add(cave2)
            if cave1 != 'start':
                cave_map[cave2].add(cave1)
    return cave_map

class CaveState:
    
    def __init__(self, location, path, visited_smalls, allowed_repeat=False):
        self.location = location
        self.path = path
        self.visited_smalls = visited_smalls
        self.allowed_repeat = allowed_repeat
    
    @classmethod
    def base_state(cls, allowed_repeat=False):
        return cls('start', [], set(), allowed_repeat=allowed_repeat)

    def next_states(self, cave_map):
        for adjacent in cave_map[self.location]:
            if is_small_cave(adjacent):
                if adjacent in self.visited_smalls:
                    if not self.allowed_repeat:
                        continue
                    else:
                        yield CaveState(adjacent, self.path + [self.location], self.visited_smalls | set([adjacent]), False)
                else:
                    yield CaveState(adjacent, self.path + [self.location], self.visited_smalls | set([adjacent]), self.allowed_repeat)
            else:
                yield CaveState(adjacent, self.path + [self.location], set(self.visited_smalls), self.allowed_repeat)
    
    def valid_moves(self, cave_map):
        return [adjacent for adjacent in cave_map[self.location] if adjacent not in self.visited_smalls]

    def __str__(self):
        if len(self.path) == 0:
            return f'({self.location})'
        if len(self.path) == 1:
            return f'{self.path[0]} -> ({self.location})'
        else:
            path_str = ' -> '.join(self.path) 
            return f'{path_str} -> ({self.location})'
    
    def __repr__(self):
        return str(self)

def is_small_cave(cave):
    return cave.islower()

from collections import deque

def find_all_paths(test_num, allow_repeat):
    breakpoint()
    cave_map = parse_cave(test_num)
    cave_state = CaveState.base_state(allow_repeat)
    state_queue = deque([cave_state])
    completed_trips = []
    while state_queue:
        current_state = state_queue.popleft()
        if current_state.location == "end":
            completed_trips.append(current_state.path + ['end'])
            continue
        next_states = list(current_state.next_states(cave_map))
        state_queue.extend(next_states)        
    return completed_trips

def print_pp(possible, pp):
    if pp:
        print("Possible paths:")
        for path in possible:
            print(' -> '.join(path))
    print(f"Count: {len(possible)}")

def part1(test_num, pp):
    possible_paths = find_all_paths(test_num, False)
    print_pp(possible_paths, pp)
    
def part2(test_num, pp):
    possible_paths = find_all_paths(test_num, True)
    print_pp(possible_paths, pp)
    
if __name__ == '__main__':
    # part1(1)    
    # part1(2)    
    # part1(3)    
    # part1(None)    

    part2(1, True)
    part2(2, True)
    part2(3, True)
    part2(None, False)