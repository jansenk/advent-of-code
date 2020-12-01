

def get_surrounding_points(p):
	pm1 = (0, 1, -1)
	results = []
	for x in pm1:
		for y in pm1:
			for z in pm1:
				if len(p) == 4:
					for w in pm1:
						if all(n == 0 for n in (x, y, z, w)):
							continue
						else:
							results.append((
								p[0] + x,
								p[1] + y,
								p[2] + z,
								p[3] + w
							))
				else:
					if all(n == 0 for n in (x, y, z)):
						continue
					else:
						results.append((
							p[0] + x,
							p[1] + y,
							p[2] + z
						))
	return results

from collections import Counter
def mutate(cubes):
	counter = Counter()
	for cube in cubes:
		counter.update(get_surrounding_points(cube))
	new_step = set()
	for neighbor, adjacent_on in counter.most_common():
		if adjacent_on > 3:
			continue
		if adjacent_on < 2:
			break
		if neighbor in cubes:
			if adjacent_on in (2, 3):
				new_step.add(neighbor)
		else:
			if adjacent_on == 3:
				new_step.add(neighbor)
	return new_step

def read_file(filename, fd=False):
	result = set()
	with open('advent/input_files/'+filename) as f:
		for y, line in enumerate(f):
			for x, char in enumerate(line):
				if char == '#':
					if not fd:
						result.add((x, y, 0))
					else:
						result.add((x, y, 0, 0))
	return result

def solve_p1(filename):
	state = read_file(filename)
	for _ in range(6):
		state = mutate(state)
	print(len(state))

# solve_p1('17.txt')

def solve_p2(filename):
	state = read_file(filename, fd=True)
	for _ in range(6):
		state = mutate(state)
	print(len(state))

solve_p2('17.txt')
