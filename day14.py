from .day10 import knot_hash_from_string
from .util import Point, move, Direction, cardinal_surrounding_points
from collections import deque
KEY = 'ffayrhll'

def hex_str_2_bin_str(hex_str):
	return ''.join([format(int(c, 16), '0=4b') for c in hex_str])

EXAMPLE_HEX2BIN_IN = 'a0c2017'
EXAMPLE_HEX2BIN_OUT = '1010000011000010000000010111'
assert hex_str_2_bin_str(EXAMPLE_HEX2BIN_IN) == EXAMPLE_HEX2BIN_OUT

def griderator(key_str):
	for i in range(128):
		row_key = key_str + '-' + str(i)
		hex_str = knot_hash_from_string(row_key)
		bin_str = hex_str_2_bin_str(hex_str)
		yield bin_str

def count_ones(key_str):
	total = 0
	for line in griderator(key_str):
		total += len(list(filter(lambda c: c == '1', line)))
	return total

assert count_ones('flqrgnkx') == 8108
print("Part One")
print(count_ones(KEY))

def make_grid(key_str):
	grid = set()
	for j, row in enumerate(griderator(key_str)):
		for i, c in enumerate(row):
			if c == '1':
				grid.add(Point(i, j))
	return grid

def count_groups(grid):
	groups = 0
	import pdb; pdb.set_trace()
	while grid:
		group_seed = grid.pop()
		groups += 1
		seen_in_group = set()
		queue = deque([group_seed])
		while queue:
			current_item = queue.popleft()
			if current_item in seen_in_group:
				continue
			try:
				grid.remove(current_item)
			except:
				pass
			seen_in_group.add(current_item)
			for neighbor in cardinal_surrounding_points(current_item):
				if neighbor in grid:
					queue.append(neighbor)
	return groups

def print_grid(grid, x, y):
	for j in range(y):
		row = []
		for i in range(x):
			if Point(i, j) in grid:
				row.append('#')
			else:
				row.append('.')
		print(''.join(row))

print("Part 2")
print("test")
test_grid = make_grid('flqrgnkx')
# print_grid(test_grid, 8, 8)
print(count_groups(test_grid))

print("answer")
grid = make_grid(KEY)
print(count_groups(grid))





