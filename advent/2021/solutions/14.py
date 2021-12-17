def parse_input(test):
    polymer_template = None
    pair_insertions = {} 
    test_str = f'-test' if test else ''
    with open(f'advent/2021/input_files/14{test_str}.txt') as f:
        polymer_template = [c for c in f.readline().strip()]
        f.readline()
        for line in f:
            pair, inserted = line.strip().split(' -> ')
            pair_insertions[(pair[0], pair[1])] = inserted
    return polymer_template, pair_insertions

def get_insertions(polymer, pair_insertions):
    insertions = []
    for i in range(len(polymer) - 1):
        pair = pair_insertions.get((polymer[i], polymer[i+1]))
        insertions.append(pair)
    return insertions

def insert_insertions(polymer, insertions):
    new_polymer = [polymer[0]]
    for insertion, polymer_element in zip(insertions, polymer[1:]):
        new_polymer.append(insertion)
        new_polymer.append(polymer_element)
    return new_polymer    

from collections import Counter
 
def synthesize(test, steps):
    # breakpoint()
    polymer_template, pair_insertions = parse_input(test)
    print(f"Template: {''.join(polymer_template)}")
    polymer = polymer_template
    for step in range(1, steps + 1):
        insertions = get_insertions(polymer, pair_insertions)
        polymer = insert_insertions(polymer, insertions)
        print(f"After step {step}: {len(polymer)} ")
    poly_count = Counter(polymer)
    most_common = (0, None)
    least_common = (float('inf'), None)
    for val, count in poly_count.items():
        if count > most_common[0]:
            most_common = (count, val)
        if count < least_common[0]:
            least_common = (count, val)
    print(f"Most common: {most_common[1]} ({most_common[0]})")
    print(f"Least common: {least_common[1]} ({least_common[0]})")
    print(most_common[0] - least_common[0])

def part1(test):
    synthesize(test, 10)

def part2(test):
    synthesize(test, 40)

if __name__ == "__main__":
    # part1(True)
    # part1(False)
    
    part2(True)
    # part2(False)

        
    