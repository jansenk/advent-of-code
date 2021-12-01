f = open("advent2017/input_files/07.txt", "r")

def parse_weight(s):
	l = len(s)
	no_paren = s[1:l-1]
	return int(no_paren)

child_to_parent = dict()
parent_to_children = dict()
program_to_weight = dict()


for line in f:
	tokens = line.split()
	program_name = tokens[0]
	tokens_weight = parse_weight(tokens[1])
	program_to_weight[program_name] = tokens_weight
	if len(tokens) > 2:
		children_with_commas = tokens[3:]
		children = []
		for i in range(len(children_with_commas)):
			child = children_with_commas[i]
			if i == len(children_with_commas) - 1:
				children.append(child)
			else:
				children.append(child[:len(child)-1])
		parent_to_children[program_name] = children
		for child in children:
			child_to_parent[child] = program_name

current_program = program_name
while True:
	try:
		current_program = child_to_parent[current_program]
	except:
		break
print(current_program)

program_to_treeweight = dict()
from collections import Counter

def try_to_identify_problem(children):
	count = Counter([program_to_treeweight[child] for child in children])
	most_common = count.most_common(2)
	if len(most_common) == 2:
		assert most_common[0][1] > most_common[1][1]
		most_common = most_common[0][0]
	else:
		raise Exception('damn')
	for child in children:
		if program_to_treeweight[child] != most_common:
			return child, most_common

def try_to_fix(program, target_weight):
	children = parent_to_children[program]
	if len(set([program_to_treeweight[child] for child in children])) == 1:
		childweights = sum([program_to_treeweight[child] for child in children])
		print(abs(target_weight - childweights))
		return True
	else:
		target_child = try_to_identify_problem(children)
		try_to_fix(target_child)
	

def check_balanced(program):
	if program not in parent_to_children:
		program_to_treeweight[program] = program_to_weight[program]
		return program_to_treeweight[program]
	child_balance = {child: check_balanced(child) for child in parent_to_children[program]}
	if len(set(child_balance.values())) != 1:
		child, target = try_to_identify_problem(parent_to_children[program])
		try_to_fix(child, target)
		raise Exception()
	else:
		treeweight = sum(child_balance.values()) + program_to_weight[program]
		program_to_treeweight[program] = treeweight
		return treeweight

check_balanced(current_program)
