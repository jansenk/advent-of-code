from ..utils import iterlines

def get_elf_calories(is_test):
    elves = []
    current_elf = 0
    for line in iterlines(1, is_test):
        line = line.strip()
        if line == '':
            elves.append(current_elf)
            current_elf = 0
        else:
            current_elf += int(line)
    elves.append(current_elf)
    return elves

test_cals = sorted(get_elf_calories(True))
cals = sorted(get_elf_calories(False))

print(test_cals[-1])
print(cals[-1])
print(sum(test_cals[len(test_cals)-3:]))
print(sum(cals[len(cals)-3:]))
