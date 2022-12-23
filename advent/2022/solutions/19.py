from collections import deque, namedtuple
from enum import Enum
from ..utils import iterlines
import re

Blueprint = namedtuple("Blueprint", ["id", "ore", "clay", "obsidian", "geode"])
class Material(Enum):
    ORE = 'ore'
    CLAY = 'clay'
    OBSIDIAN = 'obsidian'
    GEODE = 'geode'
    

PATTERN = (
    r"Blueprint (?P<id>\d+): "
    r"Each ore robot costs (?P<ore>.*?)\. "
    r"Each clay robot costs (?P<clay>.*?)\. "
    r"Each obsidian robot costs (?P<obsidian>.*?)\. "
    r"Each geode robot costs (?P<geode>.*?)\."
)
def parse_blueprints(is_test):
    bps = []
    for line in iterlines(19, is_test):
            m = re.match(PATTERN, line)
            assert m is not None
            costs = parse_costs(m)
            bp = Blueprint(
                m['id'],
                costs[Material.ORE],
                costs[Material.CLAY],
                costs[Material.OBSIDIAN],
                costs[Material.GEODE]                
            )
            bps.append(bp)
    return bps

def parse_costs(m):
    result = {}
    for mat in Material:
        robotcost = {mat.value: 0 for mat in Material}
        raw = m[mat.value]
        costs = raw.split(" and ")
        for cost in costs:
            t = cost.split(" ")
            costcost = int(t[0])
            costmat = t[1].lower()
            robotcost[costmat] = costcost
        result[mat] = robotcost
    return result

# c = parse_blueprints(True)
            

State = namedtuple(
    "State", 
    [
        "minute",
        "resources",
        "robots",
        "decisions"
    ]
)

Resources = namedtuple("Resources", ["ore", "clay", "obsidian", "geode"])
Robots = namedtuple("Robots", ["ore", "clay", "obsidian", "geode"])

def make_resources(d):
    assert isinstance(d, dict)
    return Resources(
        d['ore'],
        d['clay'],
        d['obsidian'],
        d['geode']
    )
    
def modify_resources(r1, r2, f):
    return Resources(
        f(r1[0], r2[0]),
        f(r1[1], r2[1]),
        f(r1[2], r2[2]),
        f(r1[3], r2[3]),
    )

def add_resources(r1, r2):
    return modify_resources(r1, r2, lambda a, b: a + b)

def subtract_resources(r1, r2):
    return modify_resources(r1, r2, lambda a, b: a - b)

starting_state = State(
    1,
    Resources(1, 0, 0, 0),
    Robots(1, 0, 0, 0),
    (),
)

def should_early_fail(current_state, best_geodes):
    remaining_time = 24 - current_state.minute
    possible_geode = current_state.resources.geode + (current_state.robots.geode * remaining_time) + sum(range(1, remaining_time + 1))
    return possible_geode <= best_geodes

def can_buy(bp, current_state, robot):
    for material, cost in getattr(bp, robot.value).items():
        if getattr(current_state.resources, material) < cost:
            return False
    return True        

def add_a_robot(current, new):
    current_dict = current._asdict()
    current_dict[new.value] += 1
    return Robots(**current_dict)

def possible_moves(blueprint, current_state):
    resources_gained = Resources(
        current_state.robots.ore,
        current_state.robots.clay,
        current_state.robots.obsidian,
        current_state.robots.geode,
    )
    moves = []
    for robot in Material:
        if can_buy(blueprint, current_state, robot):
            new_resources = subtract_resources(current_state.resources, make_resources(getattr(blueprint, robot.value)))
            new_resources = add_resources(new_resources, resources_gained)
            new_robots = add_a_robot(current_state.robots, robot)
            moves.append(
                State(
                    current_state.minute + 1,
                    new_resources,
                    new_robots,
                    (*current_state.decisions, robot)                        
                )
            )
    moves.append(
        State(
            current_state.minute + 1,
            add_resources(current_state.resources, resources_gained),
            current_state.robots,
            (*current_state.decisions, None)                        
        )
    )
    
    return moves

def run_bp(bp):
    q = deque([starting_state])
    best_state = starting_state
    seen_states = set()
    breakpoint()
    while q:
        current_state = q.pop()
        print(f"Current state: minute {current_state.minute}")
        if current_state in seen_states:
            continue
        elif current_state.minute == 24:
            print("Endgame, rip")
            if current_state.resources.geode > best_state.resources.geode:
                best_state = current_state
                print(f"New best state {best_state.resources.geode}")
            continue
        elif should_early_fail(current_state, best_state.resources.geode):
            print("EArly quitting")
            continue
        else:
            possible_next_states = possible_moves(bp, current_state)
            print(f"Adding {len(possible_next_states)} possible moves")
            q.extend(possible_next_states)
            seen_states.add(current_state)
    breakpoint()
    return best_state

def part1(is_test):
    bps = parse_blueprints(is_test)
    result = {}
    for bp in bps:
        best_state = run_bp(bp)
        result[bp.id] = best_state
    
part1(True)