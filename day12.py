from collections import defaultdict, deque
f = open('advent2017/input_files/12.txt', 'r')

test_input = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
def load_nodes(input_str):
	nodes = defaultdict(set)
	for line in input_str:
		tokens = line.split()
		node = tokens[0]
		for neighbor in tokens[2:]:
			last_i = len(neighbor) - 1
			if neighbor[last_i] == ',':
				neighbor = neighbor[:last_i]
			nodes[node].add(neighbor)
			nodes[neighbor].add(node)
	return nodes

def find_connected(origin, nodes):
	seen = set()
	queue = deque([origin])
	
	while queue:
		current_program = queue.popleft()
		if current_program in seen:
			continue
		else:
			seen.add(current_program)
			queue.extend(nodes[current_program])
	
	return seen

nodes = load_nodes(test_input.split('\n'))
connected = find_connected('0', nodes)
assert len(connected) == 6

nodes = load_nodes(f)
connected = find_connected('0', nodes)
print(len(connected))

groups = 0
seen_in_a_group = set()
for node in nodes:
	if node in seen_in_a_group:
		continue
	groups += 1
	node_group = find_connected(node, nodes)
	seen_in_a_group.update(node_group)

print(groups)




