correct_wirings = [
    set('abcefg'),  # 0
    set('cf'),      # 1
    set('acdeg'),   # 2
    set('acdfg'),   # 3
    set('bcdf'),    # 4
    set('abdfg'),   # 5
    set('abdefg'),  # 6
    set('acf'),     # 7
    set('abcdefg'), # 8
    set('abcdfg'),  # 9
]

segment_count_to_potential_numbers = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8],
}

def parse_input(test):
    test_str = '-test' if test else ''
    result = []
    with open(f'advent/2021/input_files/8{test_str}.txt') as f:
        for line in f:
            unique_signal_patterns, output_digits = line.split(' | ')
            unique_signal_patterns = map(set, unique_signal_patterns.strip().split())
            output_digits = map(set, output_digits.strip().split())
            result.append((unique_signal_patterns, output_digits))
    return result

def part1(test=True):
    input_lines = parse_input(test)
    simple_num_count = 0
    for _, output_digits in input_lines:
        simple_num_count += sum(1 for output_digit in output_digits if is_simple_number(output_digit))
    print(simple_num_count)

def is_simple_number(segments):
    number = get_simple_number(segments)
    return number is not None

def get_simple_number(segments):
    number = segment_count_to_potential_numbers[len(segments)]
    if len(number) != 1:
        return None
    return number[0]

def generate_number_solution(wires_mapping):
    # wires_mapping is a mapping of actul wire to "jumbled" wire
    # returns a list of sets, where index is the number and set is the "jumbled" wires that result in that number
    number_solution = []
    for correct_wiring in correct_wirings:
        number_solution.append(set(wires_mapping[correct_seg] for correct_seg in correct_wiring))
    return number_solution

def add_potential_wire_mapping(potential_wires_mapping, segment_pattern, number):
    if number == 8:
        return  # reduce noise? 
    for real_wire in correct_wirings[number]:
        potential_wires_mapping[real_wire].update(segment_pattern)

def find_superset(collection, subset):
    for item in collection:
        if item.issuperset(subset):
            return item

def solve_six_segment_patterns(numbers_mapping, six_segment_patterns):
    nine = find_nine(numbers_mapping, six_segment_patterns)
    six_segment_patterns.remove(nine)
    zero = find_zero(numbers_mapping, six_segment_patterns)
    six_segment_patterns.remove(zero)
    six = six_segment_patterns[0]
    return zero, six, nine

def find_nine(numbers_mapping, six_segment_patterns):
    # 9 is the only six-segment that's a superset of 4 + 7
    abcdf = numbers_mapping[4] | numbers_mapping[7]
    return find_superset(six_segment_patterns, abcdf)
    
def find_zero(numbers_mapping, six_segment_patterns):
    # after finding nine, zero is the remaining of the two that's a superset of 1
    return find_superset(six_segment_patterns, numbers_mapping[1])

def solve_five_segment_patterns(numbers_mapping, five_segment_patterns):
    three = find_three(numbers_mapping, five_segment_patterns)
    five_segment_patterns.remove(three)
    two = find_two(numbers_mapping, five_segment_patterns)
    five_segment_patterns.remove(two)
    five = five_segment_patterns[0]
    return two, three, five

def find_three(numbers_mapping, five_segment_patterns):
    # 3 is the only five-segment that's a superset of 1
    return find_superset(five_segment_patterns, numbers_mapping[1])

def find_two(numbers_mapping, five_segment_patterns):
    # two is the only 2-segment that contains E, which can befound with 8 - 9
    e = numbers_mapping[8] - numbers_mapping[9]
    return find_superset(five_segment_patterns, e)
    
def deduce_numbers(unique_signal_patterns):
    numbers_mapping = {} # from real number to "mixed" segments
    five_segment_patterns = []
    six_segment_patterns = []
    for unique_signal_pattern in unique_signal_patterns:
        if is_simple_number(unique_signal_pattern):
            number = get_simple_number(unique_signal_pattern)
            numbers_mapping[number] = unique_signal_pattern
        else:
            l = len(unique_signal_pattern)
            if l == 5:
                target_list = five_segment_patterns
            elif l == 6:
                target_list = six_segment_patterns
            
            if unique_signal_pattern not in target_list:
                target_list.append(unique_signal_pattern)
    
    # solve the six-segment patterns using 1 7 and 4
    zero, six, nine = solve_six_segment_patterns(numbers_mapping, six_segment_patterns)
    assert all(solved_six is not None for solved_six in (zero, six, nine))
    numbers_mapping[0] = zero
    numbers_mapping[6] = six
    numbers_mapping[9] = nine
    
    two, three, five = solve_five_segment_patterns(numbers_mapping, five_segment_patterns)
    assert all(solved_five is not None for solved_five in (two, three, five))
    numbers_mapping[2] = two
    numbers_mapping[3] = three
    numbers_mapping[5] = five
    
    return [numbers_mapping[i] for i in range(10)] 
    
def calculate_output_digits_value(output_digits, number_solution):
    #number_solution is a list of sets, where index is the number and set is the "jumbled" wires that result in that number
    output_numbers = [number_solution.index(output_digit) for output_digit in output_digits]
    output_digits_value = (output_numbers[0] * 1000) + (output_numbers[1] * 100) + (output_numbers[2] * 10) + (output_numbers[3])
    return output_digits_value

assert calculate_output_digits_value([correct_wirings[3], correct_wirings[5], correct_wirings[8], correct_wirings[0]], correct_wirings) == 3580

def part2(test=True):
    input_lines = parse_input(test)
    total_result = 0
    for unique_signal_patterns, output_digits in input_lines:
        number_solution = deduce_numbers(unique_signal_patterns)
        output = calculate_output_digits_value(output_digits, number_solution)
        # print(output)
        total_result += output
    print('--------')
    print(total_result)
    
    
    
    
# part1(test=True)
part2(test=False)
def simple_test():
    numbers = deduce_numbers(list(map(set, ['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'])))
    output = calculate_output_digits_value(list(map(set, ['cdfeb', 'fcadb', 'cdfeb', 'cdbaf'])), numbers)
    print(output)
