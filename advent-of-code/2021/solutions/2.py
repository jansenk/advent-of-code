
def parse(f):
    result = []
    for line in f:
        command, val = line.split()
        val = int(val)
        result.append((command, val))
    return result

with open('advent-of-code/2021/input_files/2.txt') as f:
    commands = parse(f)
with open('advent-of-code/2021/input_files/2-test.txt') as f:
    test_commands = parse(f)

def part1(f):
    x, y = 0, 0
    for command, val in f:
        if command == 'forward':
            x += val
        elif command == 'down':
            y += val
        elif command == 'up':
            y -= val

    print(x, y)
    print(x * y)

part1(commands)

def part2(commands):
    x, y, aim = 0, 0, 0
    for command, val in commands:
        if command == 'forward':
            x += val
            y += aim * val
        elif command == 'down':
            aim += val
        elif command == 'up':
            aim -= val

    print(x, y)
    print(x * y)

print("part 2")
part2(test_commands)
part2(commands)


    
    