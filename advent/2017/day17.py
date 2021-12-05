def make_link(skip, steps):
	forward_linked = {0:0}
	current_node = 0
	next_node_to_insert = 1
	for _ in range(steps):
		for _ in range(skip):
			current_node = forward_linked[current_node]
		t = forward_linked[current_node]
		forward_linked[current_node] = next_node_to_insert
		forward_linked[next_node_to_insert] = t
		current_node = next_node_to_insert
		next_node_to_insert += 1
	return forward_linked

def link_to_list(linked):
	current_node = 0
	result = []
	while True:
		result.append(current_node)
		if linked[current_node] == 0:
			return result
		else:
			current_node = linked[current_node]

steps = [
	[0,1],
	[0,2,1],
	[0,2,3,1],
	[0,2,4,3,1],
	[0,5,2,4,3,1],
	[0,5,2,4,3,6,1],
	[0,5,7,2,4,3,6,1],
	[0,5,7,2,4,3,8,6,1],
	[0,9,5,7,2,4,3,8,6,1]
]
for i, expected_value in enumerate(steps):
	link = make_link(3, i+1)
	l = link_to_list(link)
	assert l == expected_value

link = make_link(344, 2017)
print(link[2017])

buffer_pointer = 0
last_zero = 1
for i in range(50_000_000):
	buffer_pointer = (buffer_pointer + 344) % (i + 1)
	if buffer_pointer == 0:
		last_zero = i + 1
	buffer_pointer += 1
	buffer_pointer = (buffer_pointer) % (i + 2)
print(last_zero)
