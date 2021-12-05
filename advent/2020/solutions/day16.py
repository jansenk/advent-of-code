def iterate_until_newline(f, discard=True):
    if discard:
        f.readline() #discard heading
    while True:
        line = f.readline()
        if line is None:
            raise StopIteration
        line = line.strip()
        if line == '':
            raise StopIteration
        yield line

def matches_rule(value, rule):
    for range_min, range_max in rule:
        if range_min <= value and value <= range_max:
            return True
    return False

def solve_p1(filename):
    f = open('advent/input_files/'+filename)
    import pdb; pdb.set_trace()
    rule_ranges = []
    for rule_line in iterate_until_newline(f, False):
        tokens = rule_line.split(":")
        rule_name = tokens[0]
        for rule_range in tokens[1].split():
            if rule_range == 'or':
                continue
            range_min, range_max = rule_range.split('-')
            range_min, range_max = int(range_min), int(range_max)
            rule_ranges.append((range_min, range_max))
    
    for my_line in iterate_until_newline(f):
        continue
    
    bad_values = 0
    for nearby_line in iterate_until_newline(f):
        values = map(int, nearby_line.split(','))
        # valid = True
        for value in values:
            if not matches_rule(value, rule_ranges):
                bad_values += value
    print(bad_values)

# solve_p1('16.txt')

def solve_p2(filename):
    f = open('advent/input_files/'+filename)
    rules = dict()
    for rule_line in iterate_until_newline(f, False):
        tokens = rule_line.split(":")
        rule_name = tokens[0]
        rule_ranges = []
        for rule_range in tokens[1].split():
            if rule_range == 'or':
                continue
            range_min, range_max = rule_range.split('-')
            range_min, range_max = int(range_min), int(range_max)
            rule_ranges.append((range_min, range_max))
        rules[rule_name] = rule_ranges

    for my_line in iterate_until_newline(f):
        my_ticket = list(map(int, my_line.split(',')))
    
    good_tickets = []
    for nearby_line in iterate_until_newline(f):
        values = list(map(int, nearby_line.split(',')))
        valid = True
        for value in values:
            matches_any = False
            for rule in rules.values():
                if matches_rule(value, rule):
                    matches_any = True
                    break
            if not matches_any:
                valid = False
                break
        if valid:
            good_tickets.append(values)

    # import pdb; pdb.set_trace()

    possible_positions = [set(rules.keys()) for _ in my_ticket]
    for ticket in good_tickets + [my_ticket]:
        for i, value in enumerate(ticket):
            invalid_labels = set()
            for possible_label in possible_positions[i]:
                if not matches_rule(value, rules[possible_label]):
                    invalid_labels.add(possible_label)
            possible_positions[i] -= invalid_labels

    # import pdb; pdb.set_trace()
    prev_singletons = 0
    while True:
        singletons = [next(iter(s)) for s in possible_positions if len(s) == 1]
        assert len(singletons) == len(set(singletons))
        singletons = set(singletons)
        if len(singletons) == len(possible_positions):
            print(possible_positions)
            break
        possible_positions = [pp - singletons if len(pp) > 1 else pp for pp in possible_positions]
        prev_singletons = len(singletons)
    
    # import pdb; pdb.set_trace()
    positions = [next(iter(s)) for s in possible_positions]
    print(positions)
    s = 1
    for i, field in enumerate(positions):
        if field.startswith('departure'):
            s *= my_ticket[i]
    print(s)
solve_p2('16.txt')
