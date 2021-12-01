def _find_paren(tokens, start, modifier, increase_depth_token, decrease_depth_token):
	layers = 1
	end = start
	assert tokens[start] == increase_depth_token
	while layers != 0:
		end += modifier
		if tokens[end] == decrease_depth_token:
			layers -= 1
		elif tokens[end] == increase_depth_token:
			layers += 1
	return end


def find_matching_paren(tokens, i):
	return _find_paren(tokens, i, 1, "(", ")")

def find_matching_paren_backwards(tokens, j):
	return _find_paren(tokens, j, -1, ")", "(")

test_parens = 'asdfa( asdfa(asdf(()asdfa)a) asdfasd(asdfa ) )asdfa(asdf)'
matches = [(5, 45), (12, 27), (17, 25), (18, 19), (36, 43), (51, 56)]
for opening_i, closing_i in matches:
	assert find_matching_paren(test_parens, opening_i) == closing_i
	assert find_matching_paren_backwards(test_parens, closing_i) == opening_i

op_map = {
	"+": lambda a, b: a + b,
	"-": lambda a, b: a - b,
	"*": lambda a, b: a * b,
	"/": lambda a, b: a / b
}
def math(tokens, leftmost, rightmost):
	# import pdb; pdb.set_trace()
	current_token = tokens[rightmost]
	current_value = None
	if current_token == ")":
		matching_paren = find_matching_paren_backwards(tokens, rightmost)
		current_value = math(tokens, matching_paren+1, rightmost-1)
		rightmost = matching_paren
	else:
		current_value = current_token
	
	if rightmost <= leftmost:
		return current_value
	else:
		operation = tokens[rightmost-1]
		other_value = math(tokens, leftmost, rightmost-2)
		return op_map[operation](current_value, other_value)

def parse_math_input(line):
	return [int(a) if a.isdigit() else a for a in line if a != ' ']

def do_math(line):
	tokens = parse_math_input(line)
	r = math(tokens, 0, len(tokens) - 1)
	# print(r)
	return r

test_inputs = []
assert do_math('1 + 2 + 3') == 6
assert do_math('1 + 2 * 3 + 4 * 5 + 6') == 71
assert do_math('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert do_math('2 * 3 + (4 * 5)') == 26
assert do_math('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert do_math('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert do_math('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

def sum_of_mathlines(filename):
	result = 0
	for line in open('advent/input_files/'+filename):
		try:
			result += do_math(line.strip())
		except:
			print(line)
			return
	print(result)

sum_of_mathlines('18.txt')

assert do_math('(((3)))') == 3
assert do_math('((1 + (2 * 3)) + (4 * (5 + 6)))') == 51
assert do_math('2 * (3 + (4 * 5))') == 46
assert do_math('(5 + (8 * ((3 + 9) + 3) * 4 * 3))')  == 1445
assert do_math('5 * 9 * (7 * 3 * (3 + 9) * (3 + (8 + 6 * 4)))') == 669060
assert do_math('(((((2 + 4) * 9) * (((6 + 9) * (8 + 6)) + 6)) + 2) + 4) * 2') == 23340

def add_parens(tokens):
	# import pdb; pdb.set_trace()
	j = len(tokens)
	i = 0
	while i < j:
		token = tokens[i]
		if token == '+':
			left_entity = tokens[i-1]
			right_entity = tokens[i+1]
			if isinstance(left_entity, int):
				left_i = i - 1
			else:
				assert left_entity == ')'
				left_i = find_matching_paren_backwards(tokens, i -1)
			if isinstance(right_entity, int):
				right_i = i + 2
			else:
				assert right_entity == '('
				right_i = find_matching_paren(tokens, i + 1) + 1
			#slowly, carefully
			tokens.insert(left_i, '(')
			i += 1
			j += 1
			right_i += 1
			tokens.insert(right_i, ')')
			j += 1
		i += 1
	return tokens

def do_advanced_math(line):
	tokens = parse_math_input(line)
	tokens = add_parens(tokens)
	r = math(tokens, 0, len(tokens) - 1)
	# print(r)
	return r

do_advanced_math('1 + 2 + 3')
do_advanced_math('1 + 2 * 3 + 4 * 5 + 6')
do_advanced_math('1 + (2 * 3) + (4 * (5 + 6))')
do_advanced_math('2 * 3 + (4 * 5)')
do_advanced_math('5 + (8 * 3 + 9 + 3 * 4 * 3)')
do_advanced_math('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')
do_advanced_math('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')

def sum_of_advanced_mathlines(filename):
	result = 0
	for line in open('advent/input_files/'+filename):
		try:
			result += do_advanced_math(line.strip())
		except:
			print(line)
			return
	print(result)

sum_of_advanced_mathlines('18.txt')