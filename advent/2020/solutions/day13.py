from math import ceil

def bus_leave_time(start_time, bus_id):
	return ceil(start_time/bus_id) * bus_id

def bus_wait_time(start_time, bus_id):
	time_since_last_bus = (start_time % bus_id)
	if time_since_last_bus == 0:
		return 0
	return bus_id - time_since_last_bus

assert bus_wait_time(939, 7) == 6
assert bus_wait_time(938, 7) == 0
assert bus_wait_time(939, 59) == 5

def find_next_bus(filename):
	with open('advent/input_files/'+filename) as f:
		start_time = int(f.readline())
		buses = f.readline().split(',')
		shortest_wait = float('inf')
		shortest_wait_id = None
		for bus_id in buses:
			if bus_id == 'x':
				continue
			else:
				bus_id = int(bus_id)
			wait_time = bus_wait_time(start_time, bus_id)
			if wait_time < shortest_wait:
				shortest_wait = wait_time
				shortest_wait_id = bus_id
		print(shortest_wait_id * shortest_wait)

find_next_bus('13.txt')

def solve_remainder_theory(values):
	"""given a list of (a, b) such that x = a (mod b)"""

	remainder_theorem_table = {
		'mod': [b for _, b in values],
		'bi': [a for a, _ in values],
		'Ni': [],
		'xi': [],
	}

	N = 1
	for mod in remainder_theorem_table['mod']:
		N *= mod
	
	remainder_theorem_table['Ni'] = [int(N/mod) for mod in remainder_theorem_table['mod']]
	total = 0
	for i, Ni in enumerate(remainder_theorem_table['Ni']):
		xi = 1
		while True:
			if (Ni * xi) % remainder_theorem_table['mod'][i] == 1:
				break
			else:
				xi += 1
		total += remainder_theorem_table['bi'][i] * Ni * xi
	return total, total % N

print(solve_remainder_theory([(3, 5), (1, 7), (6, 8)]))

def do_the_stupid_remainder_theorem(filename):
	with open('advent/input_files/'+filename) as f:
		_ = int(f.readline())
		buses = [int(n) if n != 'x' else None for n in f.readline().split(',')]
	values = []
	for i, bus_id in enumerate(buses):
		if bus_id is not None:
			values.append((bus_id - i if i > 0 else 0, bus_id))
	val = solve_remainder_theory(values)
	print(val)

do_the_stupid_remainder_theorem('13.txt')
