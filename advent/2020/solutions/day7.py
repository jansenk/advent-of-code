import pdb
def parse_bagtree_line(line):
	line = line.strip()
	target_color, remainder = line.split(" bags contain ")
	# if target_color == 'faded blue':
	# 	pdb.set_trace()
	if remainder == "no other bags.":
		children = []
	else:
		remainder = remainder[:len(remainder)-1] # trim period
		if ',' not in remainder:
			children = [remainder]
		else:
			children = remainder.split(', ')
	result = []
	for child in children:
		number, color, color2, _  = child.split()
		result.append((int(number), " ".join((color, color2))))
	return target_color, result

testlines = [
	'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
	'bright white bags contain 1 shiny gold bag.',
	'dotted black bags contain no other bags.'
]
assert parse_bagtree_line(testlines[0]) == ('dark orange', [(3, 'bright white'), (4, 'muted yellow')]) 
assert parse_bagtree_line(testlines[1]) == ('bright white', [(1, 'shiny gold')])
assert parse_bagtree_line(testlines[2]) == ('dotted black', [])

from collections import defaultdict
def build_bagtree(filename):
	parent_to_children = dict()
	child_to_parent = defaultdict(set)

	with open('advent/input_files/' + filename) as f:
		for line in f:
			try:
				color, children = parse_bagtree_line(line)
			except Exception as e:
				print(line)
				raise
			parent_to_children[color] = children
			for child in children:
				child_to_parent[child[1]].add(color)
	return parent_to_children, child_to_parent


def count_parents():
	stack = list(c2p['shiny gold'])
	parent_count = 0
	seen_parents = set()
	while stack:
		current_node = stack.pop()
		if current_node in seen_parents:
			continue
		parent_count += 1
		seen_parents.add(current_node)
		current_node_parents = c2p[current_node]
		stack.extend(current_node_parents)
	return parent_count



def count_total_children():
	# pdb.set_trace()
	total_contained_bags = dict()
	def get_total_bags(color):
		# pdb.set_trace()
		nonlocal total_contained_bags
		if color not in total_contained_bags:
			if not p2c[color]:
				total_contained_bags[color] = 0
			else:
				total_contained_bags[color] =  sum(child_number + (child_number * get_total_bags(child_color)) for child_number, child_color in p2c[color])
			# print(f'{color}: {total_contained_bags[color]}')
		return total_contained_bags[color]
	return get_total_bags('shiny gold')

p2c, c2p = build_bagtree('7.1.txt')
assert count_parents() == 4
assert count_total_children() == 32

p2c, c2p = build_bagtree('7.txt')
print(count_parents())
print(count_total_children())
