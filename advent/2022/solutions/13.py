from functools import cmp_to_key
from ..utils import iterlines

def clean_next(lines):
    try:
        return next(lines)
    except StopIteration:
        return None

def parse(is_test):
    lines = iterlines(13, is_test)
    inputs = []
    while (first_line := clean_next(lines)) is not None:
        second_line = clean_next(lines)
        inputs.append((eval(first_line), eval(second_line)))
        clean_next(lines)
    return inputs

def compare_ints(left, right, level=0, should_print=False):
    if should_print:
        print_cmp(left, right, level)
    tabs = "\t" * level
    if left < right:
        if should_print:
            print(f"{tabs}-Left side is smaller so inputs are in the right order")
        return True
    elif left > right:
        if should_print:
            print(f"{tabs}-Right side is smaller so inputs are in the wrong order")
        return False
    else:
        return None

def print_cmp(left, right, level):
    tabs = "\t" * level
    print(f"{tabs}- Compare {str(left)} vs {str(right)}")


def compare_lists(left, right, level=0, should_print=False):
    if should_print:
        print_cmp(left, right, level)
    min_len = min(len(left), len(right))
    for i in range(min_len):
        result = compare(left[i], right[i], level + 1, should_print)
        if result is not None:
            return result
    return compare_ints(len(left), len(right), level, should_print)

def compare(left, right, level=0, should_print=False):
    if isinstance(left, int) and isinstance(right, int):
        return compare_ints(left, right, level, should_print)
    elif isinstance(left, list) and isinstance(right, list):
        return compare_lists(left, right, level, should_print)
    else:
        tabs = "\t" * level
        if should_print:
            print(f"{tabs}- Mixed types; retrying")
        list_left = left
        list_right = right
        
        if isinstance(left, int):
            list_left = [left]
            assert isinstance(right, list)
        elif isinstance(right, int):
            list_right = [right]
            assert isinstance(left, list)
        
        return compare_lists(list_left, list_right, level, should_print)

def part1(is_test):
    inputs = parse(is_test)
    correct = []
    for i, (left, right) in enumerate(inputs):
        print(f"== Pair {i+1} ==")
        result = compare(left, right, should_print=True)
        if result:
            correct.append(i + 1)
        print()
    print(correct)
    print(sum(correct))

def compare_cmp(left, right):
    result = compare(left, right)
    if result:
        return -1
    elif result is None:
        return 0
    else:
        return 1
        
def part2(is_test):
    inputs = parse(is_test)
    divider_packets = [
        [[2]],
        [[6]]
    ]
    all_inputs = [divider_packets[0], divider_packets[1]]
    for left, right in inputs:
        all_inputs.append(left)
        all_inputs.append(right)
    
    all_inputs.sort(key=cmp_to_key(compare_cmp))
    for inputs in all_inputs:
        print(inputs)
    
    divider_indices = [
        all_inputs.index(divider_packets[0]),
        all_inputs.index(divider_packets[1])
    ]
    print(divider_indices)
    print((divider_indices[0] + 1) * (divider_indices[1] + 1))

part2(False)