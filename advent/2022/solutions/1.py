def get_elf_calories(filename):
    elves = []
    with open("advent/2022/input_files/" + filename) as f:
        current_elf = 0
        for line in f:
            line = line.strip()
            if line == '':
                elves.append(current_elf)
                current_elf = 0
            else:
                current_elf += int(line)
        elves.append(current_elf)
    return elves

test_cals = sorted(get_elf_calories('1_test.txt'))
cals = sorted(get_elf_calories('1.txt'))

print(test_cals[-1])
print(cals[-1])
print(sum(test_cals[len(test_cals)-3:]))
print(sum(cals[len(cals)-3:]))
