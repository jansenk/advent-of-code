def parse_lines(test):
    test_str = '-test' if test else ''
    with open(f'advent/2021/input_files/10{test_str}.txt') as f:
        return list(map(lambda l: l.strip(), f.readlines()))

corrupted_scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
incomplete_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}
bracket_matches = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>',
}

from collections import deque
CORRUPTED = 'corr'
INCOMPLETE = 'inc'
COMPLETE = 'compl'

def is_opening_brace(c):
    return c in '({[<'

def is_closing_brace(c):
    return c in ')}]>'

def get_matching_closing_brace(c):
    return bracket_matches[c]

def analyze_line(line):
    stack = deque()
    for c in line:
        if is_opening_brace(c):
            stack.append(c)
        elif is_closing_brace(c):
            paired_opening_brace = stack.pop()
            correct_closing_brace = get_matching_closing_brace(paired_opening_brace)
            if c != correct_closing_brace:
                return CORRUPTED, c
    if stack:
        return INCOMPLETE, stack
    else:
        return COMPLETE, None

def complete_line(unmatched):
    autocomplete = []
    while unmatched:
        autocomplete.append(get_matching_closing_brace(unmatched.pop()))
    return autocomplete

def corrupted_score(corrupted_char):
    return corrupted_scores[corrupted_char]
    
def autocomplete_score(autocomplete):
    score = 0
    for c in autocomplete:
        score *= 5
        score += incomplete_scores[c]
    return score
    
def analyze_lines(test):
    lines = parse_lines(test)
    corrupted_scores, autocomplete_scores = [], []
    for line in lines:
        line_result, extra = analyze_line(line)
        if line_result == CORRUPTED:
            corrupted_scores.append(corrupted_score(extra))
        elif line_result == INCOMPLETE:
            autocomplete = complete_line(extra)
            autocomplete_scores.append(autocomplete_score(autocomplete))

    corrupted_score_result = sum(corrupted_scores)
    
    autocomplete_scores.sort()
    autocomplete_score_result = autocomplete_scores[int(len(autocomplete_scores)/2)]
    
    return corrupted_score_result, autocomplete_score_result

if __name__ == '__main__':
    corrupted, automplete = analyze_lines(True)
    print('Test: ')
    print(f'\tCorrupted score: {corrupted}')
    print(f'\tAutocomplete score: {automplete}')
    
    corrupted, automplete = analyze_lines(False)
    print('Solution: ')
    print(f'\tCorrupted score: {corrupted}')
    print(f'\tAutocomplete score: {automplete}')
