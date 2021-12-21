def parse_snailfish_number(string):
    snailfish_number, _ = _parse_snailfish_number(string)
    return snailfish_number

def _parse_snailfish_number(string, i=0, parent=None):
    assert string[i] == '['
    snailfish_number = SnailfishNumber()
    left, i = parse_child(string, i+1, snailfish_number)
    right, i = parse_child(string, i+1, snailfish_number)
    assert string[i] == ']'
    snailfish_number.left = left
    snailfish_number.right = right
    snailfish_number.parent = parent
    return snailfish_number, i+1

def parse_child(string, i, parent):
    if string[i].isdigit():
        return SnailfishValue(int(string[i]), parent), i+1
    else:
        return _parse_snailfish_number(string, i, parent=parent)
    
class SnailfishValue:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent
    
    def rightmost_value(self):
        return self
    def leftmost_value(self):
        return self
    def is_value(self):
        return True
    def __str__(self):
        return str(self.value)
    def __repr__(self) -> str:
        return str(self)
    
    def split(self):
        result = SnailfishNumber()
        left = int(self.value / 2)
        if self.value % 2 == 0:
            right = left
        else:
            right = left + 1
        result.right = SnailfishValue(right, result)
        result.left = SnailfishValue(left, result)
        result.parent = self.parent
        self.parent.replace_child(self, result)

    def _find_split(self):
        if self.value >= 10:
            return self
        return None
    
    def _find_explode(self, _):
        return None
    
    def magnitude(self):
        return self.value
        

class SnailfishNumber:
    LEFT = 'l'
    RIGHT = 'r'
    EXPLODE = 'e'
    SPLIT = 's'

    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
    
    def replace_child(self, child_requester, replacement):
        if child_requester == self.left:
            self.left = replacement
        else:
            self.right = replacement

    def is_value(self):
        return False
    
    def is_simple(self):
        return self.left.is_value() and self.right.is_value()
    
    def get_next_to_the_left(self, child_requester):
        if child_requester == self.right:
            return self.left.rightmost_value()
        elif self.parent == None:
            return None
        else:
            return self.parent.get_next_to_the_left(self)
    
    def get_next_to_the_right(self, requester):
        if requester == self.left:
            return self.right.leftmost_value()
        elif self.parent == None:
            return None
        else:
            return self.parent.get_next_to_the_right(self)
    
    def rightmost_value(self):
        return self.right.rightmost_value()
    
    def leftmost_value(self):
        return self.left.leftmost_value()
    
    def find_resolution_target(self):
        assert self.parent == None
        explode = self._find_explode(0)
        if explode:
            return self.EXPLODE, explode
        split = self._find_split()
        if split is not None:
            return self.SPLIT, split
        return None, None

    def _find_explode(self, depth):
        if depth >= 4 and self.is_simple():
            return self
        explode = self.left._find_explode(depth+1)
        if explode:
            return explode
        explode = self.right._find_explode(depth+1)
        if explode:
            return explode
        return None

    def _find_split(self):
        split = self.left._find_split()
        if split is not None:
            return split
        split = self.right._find_split()
        if split is not None:
            return split
        return None

    def do_explode(self):
        assert self.is_simple()
        next_left = self.get_next_to_the_left(self)
        next_right = self.get_next_to_the_right(self)
        if next_left is not None:
            next_left.value += self.left.value
        if next_right is not None:
            next_right.value += self.right.value
        self.parent.replace_child(self, SnailfishValue(0, self.parent))
            
    @staticmethod
    def do_resolution(type, target):
        if type == SnailfishNumber.EXPLODE:
            target.do_explode()
        else:
            target.split()

    def magnitude(self):
        return (3 * self.left.magnitude()) + (2 * self.right.magnitude())
    
    def __str__(self) -> str:
        return f"[{str(self.left)},{self.right}]"
    def __repr__(self) -> str:
        return str(self)
    def __add__(self, other):
        parent = SnailfishNumber()
        self.parent = parent
        other.parent = parent
        parent.left = self
        parent.right = other
        return parent

def test_parse():
    tests = [
        '[1,2]',
        '[[1,2],3]',
        '[9,[8,7]]',
        '[[1,9],[8,5]]',
        '[[[[1,2],[3,4]],[[5,6],[7,8]]],9]',
        '[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]',
        '[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]',
    ]
    for test in tests:
        sfn = parse_snailfish_number(test)
        assert str(sfn) == test
    print("> Parsing tests all pass")
    
def test_explode():
    tests = [
        ('[[[[[9,8],1],2],3],4]', (9, 8), '[[[[0,9],2],3],4]'),
        ('[7,[6,[5,[4,[3,2]]]]]', (3, 2), '[7,[6,[5,[7,0]]]]'),
        ('[[6,[5,[4,[3,2]]]],1]', (3, 2), '[[6,[5,[7,0]]],3]'),
        ('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', (7, 3), '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'),
        ('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', (3, 2), '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'),
    ]
    for i, (input, (expected_left, expected_right), output) in enumerate(tests):
        sfn = parse_snailfish_number(input)
        result = sfn.find_resolution_target()
        assert result is not None, i
        assert result[0] == SnailfishNumber.EXPLODE, i
        assert result[1].is_simple(), i
        assert result[1].left.value == expected_left, i
        assert result[1].right.value == expected_right, i
        
        result[1].do_explode()
        assert str(sfn) == output, i
    print("> Explode tests all pass")

def reduce_number(number):
    while True:
        reduce_type, target = number.find_resolution_target()
        if reduce_type is None:
            return
        else:
            SnailfishNumber.do_resolution(reduce_type, target)

def test_reduce():
    inputs = ('[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]')
    number_1 = parse_snailfish_number(inputs[0])
    number_2 = parse_snailfish_number(inputs[1])
    test_number = number_1 + number_2
    assert str(test_number) == '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'
    test_steps = [
        (SnailfishNumber.EXPLODE, '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]'),
        (SnailfishNumber.EXPLODE, '[[[[0,7],4],[15,[0,13]]],[1,1]]'),
        (SnailfishNumber.SPLIT, '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'),
        (SnailfishNumber.SPLIT, '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'),
        (SnailfishNumber.EXPLODE, '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
    ]
    for i, (expected_type, expected_after) in enumerate(test_steps):
        actual_type, actual_target = test_number.find_resolution_target()
        assert actual_type == expected_type, i
        SnailfishNumber.do_resolution(actual_type, actual_target)
        assert str(test_number) == expected_after, i
    actual_type, actual_target = test_number.find_resolution_target()
    assert actual_type is None
    
    test_number = number_1 + number_2
    reduce_number(test_number)
    assert str(test_number) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
    print('> reduce test passes')

def sum_file(test=None):
    test_str = f'-test{test}' if test is not None else ''
    with open(f'advent/2021/input_files/18{test_str}.txt') as f:
        first_line = f.readline().strip()
        number = parse_snailfish_number(first_line)
        for line in f:
            line = line.strip()
            number = number + parse_snailfish_number(line)
            reduce_number(number)
        return number

def test_sum_file():
    expected_results = [
        '[[[[1,1],[2,2]],[3,3]],[4,4]]',
        '[[[[3,0],[5,3]],[4,4]],[5,5]]',
        '[[[[5,0],[7,4]],[5,5]],[6,6]]',
        '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]',
    ]
    for i, expected_result in enumerate(expected_results, 1):
        result = sum_file(i)
        assert str(result) == expected_result, i
    print("> all sum file tests pass")

def test_magnitude():
    tests = [
        ('[9,1]', 29),
        ('[1,9]', 21),
        ('[[9,1],[1,9]]', 129),
        ('[[1,2],[[3,4],5]]', 143),
        ('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]', 1384),
        ('[[[[1,1],[2,2]],[3,3]],[4,4]]', 445),
        ('[[[[3,0],[5,3]],[4,4]],[5,5]]', 791),
        ('[[[[5,0],[7,4]],[5,5]],[6,6]]', 1137),
        ('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]', 3488)
    ]
    for test_input, expected_magnitude in tests:
        number = parse_snailfish_number(test_input)
        assert number.magnitude() == expected_magnitude, test_input
    print("> magnitude tests all pass")
    
def part1_test():
    number = sum_file(5)
    assert str(number) == '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]'
    assert number.magnitude() == 4140
    print('> part1 test passes')

def get_largest_two(test=None):
    test_str = f'-test{test}' if test is not None else ''
    with open(f'advent/2021/input_files/18{test_str}.txt') as f:
        numbers = [line.strip() for line in f]
    largest_lines = None
    largest_number = None
    largest_magnitude = 0
    for a in range(len(numbers)):
        for b in range(len(numbers)):
            if a == b:
                continue
            result = parse_snailfish_number(numbers[a]) + parse_snailfish_number(numbers[b])
            reduce_number(result)
            magnitude = result.magnitude()
            if magnitude > largest_magnitude:
                largest_lines = (parse_snailfish_number(numbers[a]), parse_snailfish_number(numbers[b]))
                largest_number = result
                largest_magnitude = magnitude
    return (
        *largest_lines,
        largest_number,
        largest_magnitude
    )

def part2_test():
    result = get_largest_two(5)
    a = result[0]
    b = result[1]
    largest_number = result[2]
    largest_magnitude = result[3]
    assert str(a) == '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]'
    assert str(b) == '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]'
    assert str(largest_number) == '[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]'
    assert largest_magnitude == 3993
    print("> part two test passes")
    
def run_tests():
    test_parse()
    test_explode()
    test_reduce()
    test_sum_file()
    test_magnitude()
    part1_test()
    part2_test()
    print("> all Tests pass")


if __name__ == "__main__":
    run_tests()
    number = sum_file()
    print(number.magnitude())
    result = get_largest_two()
    print(result[3])
