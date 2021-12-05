# this code is shit but i was actually trying to see how quickly i could solve at midnight
# the answer is ... like 14 minutes

with open('advent/input_files/6.txt') as f:
    sets = []
    current_set = set()
    def complete_set():
        global sets
        global current_set
        sets.append(current_set)
        current_set = set()
    for line in f:
        if line == '\n':
            complete_set()
        else:
            current_set.update(line.strip())
    complete_set()

# print(sets)
print(sum(map(len, sets)))

from collections import Counter
with open('advent/input_files/6.txt') as f:
    sets = []
    current_set = Counter()
    def complete_set():
        global sets
        global current_set
        all_yes = {v for v, c in current_set.items() if c == line_counter}
        sets.append(all_yes)
        current_set = Counter()
    line_counter = 0
    for line in f:
        if line == '\n':
            complete_set()
            line_counter = 0
        else:
            current_set.update(line.strip())
            line_counter += 1
    complete_set()

print(sum(map(len, sets)))
