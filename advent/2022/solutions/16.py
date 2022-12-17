from functools import partial, partialmethod
from itertools import permutations
from math import factorial
from typing import Dict, List
from ..utils import iterlines
from re import match, Match
from ..utils import dijkstra
INPUT_PATTERN = r"Valve (?P<valve_name>..) has flow rate=(?P<flow>\d+); tunnels? leads? to valves? (?P<tunnels>(.*))"

CaveMap = Dict[str, List[str]]

class Cave:
    
    @staticmethod
    def parse(is_test:bool):
        cave_map:CaveMap = {}
        valve_pressures:Dict[str:int] = {}
        for line in iterlines(16, is_test):
            m = match(INPUT_PATTERN, line)
            assert m is not None
            valve = m["valve_name"]
            valve_pressures[valve] = int(m['flow'])
            cave_map[valve] = list(m['tunnels'].split(", "))
        return Cave(cave_map, valve_pressures)
    
    def __init__(self, cave_map:CaveMap, valve_pressures:Dict[str,int], total_time=30):
        self.total_time = 30
        self.cave_map = cave_map
        self.valve_pressures = valve_pressures
        self.nonzero_valves = {
            node for node, valve_pressure in self.valve_pressures.items()
            if valve_pressure > 0
        }
        self.precompiled_paths = None
        self.precompile_paths()
    
    def precompile_paths(self):
        if self.precompiled_paths is not None:
            print("already done")
            return
        self.precompiled_paths = {}
        get_neighbors = lambda n: self.cave_map[n]
        travel_cost = lambda a, b: 1
        
        for node in self.cave_map:
            distances, _ = dijkstra(
                node,
                get_neighbors,
                travel_cost
            )
            self.precompiled_paths[node] = distances
    
    def get_distance(self, a, b):
        return self.precompiled_paths[a][b]

    def get_total_valve_relief(self, node, t):
        # Get the cumulative value of releasing the valve at `node` on minute `t`
        # The minus one is because the actual value does not happen until the minute after you take
        #  the action to open the valve.
        return max(0, self.valve_pressures[node] * ((self.total_time - t) - 1))
    

def get_next_steps(cave:Cave, t, current_position, opened_valves):
    result = {}
    for node in cave.nonzero_valves:
        if node == current_position:
            continue
        if node in opened_valves:
            continue
        distance = cave.get_distance(current_position, node)
        value = cave.get_total_valve_relief(node, t + distance)
        result[node] = (distance, value)
    return result

def get_lifetime_val(cave, nodes):
    current_minute = 0
    current_location = 'AA'
    open_valves = set()
    lifetime_value = 0
    for node in nodes:
        next_steps = get_next_steps(cave, current_minute, current_location, open_valves)
        distance, value = next_steps[node]
        next_minute = current_minute + distance + 1
        if next_minute >= 30:
            break
        current_minute = next_minute
        current_location = node
        lifetime_value += value
    return lifetime_value, current_minute

def tests():
    cave = Cave.parse(True)
    assert cave.get_total_valve_relief("BB", 1) == 364
    breakpoint()

def part1(is_test):
    cave = Cave.parse(is_test)
    highest_val = 0
    for i in range(1, len(cave.nonzero_valves) + 1):
        print(f"Checking all {i}-length solutions")
        for i, solution in enumerate(permutations(cave.nonzero_valves, i)):
            if i % 1000 == 0:
                print(i)
            
            val, min = get_lifetime_val(cave, solution)
            if val > highest_val:
                print(f"New highest: {str(solution)} {val}")
                highest_val = val
    print(highest_val)
    
# I literally just brute forced this. 
# never finished with permutations of size six, just tried the bigegst one from 5 and it was correct
# not even gonna attempt thinking about part 2
# not sure how i'd even brute force it

part1(False)