test_crabs = [16,1,2,0,4,2,7,1,2,14]

def parse_crabs():
    with open('advent/2021/input_files/7.txt') as f:
        return list(map(int, f.readline().split(',')))

from collections import Counter
def find_minimum_move(crabs, constant_gas=True, v=True):
    min_crab_x = min(crabs)
    max_crab_x = max(crabs)
    crab_count = Counter(crabs)
    
    if constant_gas:
        gas_cost_fn = lambda x : x
    else:
        gas_cost_fn = sumn
    
    min_gas, min_gas_x = float('inf'), 0
    for potential_x in range(min_crab_x, max_crab_x + 1):
        required_gas = get_required_gas(potential_x, crab_count, gas_cost_fn)
        if v:
            print(f'Horizontal coordinate {potential_x} requires {required_gas} gas')
        if required_gas < min_gas:
            if v:
                print('New min required gas!')
            min_gas, min_gas_x = required_gas, potential_x
    print(f'Minimum Gas Required = {min_gas} @ {min_gas_x}')
    return min_gas, min_gas_x
    
def get_required_gas(target_x, crab_count, gas_cost_fn):
    total_gas = 0
    for crab_x, num_crabs in crab_count.items():
        step_gas_cost = gas_cost_fn(abs(crab_x - target_x))
        step_required_gas = num_crabs * step_gas_cost
        total_gas += step_required_gas
    return total_gas


def sumn(n):
    return int((n * (n+1)) / 2)
    
    
# test_count = Counter(test_crabs)
# get_required_gas(2, test_count)
find_minimum_move(test_crabs, constant_gas=False, v=False)
find_minimum_move(parse_crabs(), constant_gas=False, v=False)