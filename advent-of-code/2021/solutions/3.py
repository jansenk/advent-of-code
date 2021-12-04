with open('advent-of-code/2021/input_files/3.txt') as f:
    numbers = []
    for line in f:
        numbers.append(line.strip())
with open('advent-of-code/2021/input_files/3-test.txt') as f:
    test_numbers = []
    for line in f:
        test_numbers.append(line.strip())


def count_bits(numbers):
    bit_count = [0] * len(numbers[0])
    for number in numbers:
        for i in range(len(number)):
            if number[i] == '0':
                bit_count[i] -= 1
            else:
                bit_count[i] += 1
    return bit_count

def part_1(numbers):
    part_1_count = count_bits(numbers)
    gamma = [1 if j > 0 else 0 for j in part_1_count]
    epsilon = [1 if j < 0 else 0 for j in part_1_count]

    gamma = ''.join(map(str, gamma))
    epsilon = ''.join(map(str, epsilon))

    gamma_int = int(gamma, 2)
    epsilon_int = int(epsilon, 2)

    print(f'gamma = b{gamma} = {gamma_int}')
    print(f'epsilon = b{epsilon} = {epsilon_int}')

    print(gamma_int * epsilon_int)

part_1(numbers)

def filter_helper(numbers, target_bit, keep_most_common, tie_breaker):
    bit_count = count_bits(numbers)
    if bit_count[target_bit] == 0:
        target_bit_value = tie_breaker
    else:
        most_common_value = '1' if bit_count[target_bit] > 0 else '0'
        least_common_value = '1' if most_common_value == '0' else '0'
        target_bit_value = most_common_value if keep_most_common else least_common_value
    
    new_numbers = [number for number in numbers if number[target_bit] == target_bit_value]
    return new_numbers
    
def oxygen_filter(numbers, target_bit):
    return filter_helper(numbers, target_bit, True, '1')

def co2_filter(numbers, target_bit):
    return filter_helper(numbers, target_bit, False, '0')

def find_filter_value(numbers, filter_function):
    for target_bit in range(len(numbers[0])):
        numbers = filter_function(numbers, target_bit)
        if len(numbers) == 1:
            return numbers[0]

def part_2(numbers):
    o2_value = find_filter_value(numbers, oxygen_filter)
    co2_value = find_filter_value(numbers, co2_filter)
                    
    o2_int = int(o2_value, 2)
    co2_int = int(co2_value, 2)
    
    print(f'o2 = b{o2_value} = {o2_int}')
    print(f'co2 = b{co2_value} = {co2_int}')

    print(o2_int * co2_int)
    
part_2(numbers)

    
