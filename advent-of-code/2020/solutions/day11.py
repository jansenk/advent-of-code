from ..util import Point, move, Direction, surrounding_points

def get_floor(filename):
	floor = dict()
	with open('advent/input_files/'+ filename) as f:
		for y, line in enumerate(f):
			for x, char in enumerate(line):
				if char == 'L':
					floor[Point(x, y)] = False
				if char == '#':
					floor[Point(x, y)] = True
	return floor, x, y

def print_map(chairs, mx, my):
	for y in range(my):
		line = ''
		for x in range(mx):
			p = Point(x, y)
			if p in chairs:
				if chairs[p]:
					line += "#"
				else:
					line += "L"
			else:
				line += '.'
		print(line)
	print('\n')

# chairs = get_floor('11.1.txt')
# print_map(chairs, 10, 10)

def count_surrounding_on(chairs, p):
	return sum(1 for neighbor in surrounding_points(p) if neighbor in chairs and chairs[neighbor])

def evolve(chairs):
	next_step = dict()
	stable = True
	for chair, chair_on in chairs.items():
		neighbors_on = count_surrounding_on(chairs, chair)
		if chair_on and neighbors_on >= 4:
			stable = False
			next_step[chair] = False
		elif not chair_on and neighbors_on == 0:
			stable = False
			next_step[chair] = True
		else:
			next_step[chair] = chair_on
	return next_step, stable

def find_stable(filename):
	chairs, _, _ = get_floor(filename)
	stable = False
	while not stable:
		chairs, stable = evolve(chairs)
	print(len(list(filter(lambda on: on, chairs.values()))))

# find_stable('11.1.txt')
# find_stable('11.txt')
def is_in_grid(p, maxx, maxy):
	return p.x >= 0 and p.x <= maxx and p.y >= 0 and p.y <= maxy

def count_pov_on(chairs, chair, maxx, maxy):
	count = 0
	for d in Direction.ALL_DIRECTIONS:
		current_neighbor = move(chair, d)
		sees_occupied_neighbor = False
		while is_in_grid(current_neighbor, maxx, maxy):
			if current_neighbor in chairs:
				sees_occupied_neighbor = chairs[current_neighbor]
				break
			else:
				current_neighbor = move(current_neighbor, d)
		if sees_occupied_neighbor:
			count += 1
	return count

# chairs, maxx, maxy = get_floor('11.3.txt')
# print_map(chairs, 10, 10)
# print(count_pov_on(chairs, Point(3, 3), maxx, maxy))

def evolve2(chairs, maxx, maxy):
	next_step = dict()
	stable = True
	for chair, chair_on in chairs.items():
		neighbors_on = count_pov_on(chairs, chair, maxx, maxy)
		# print(f'{chair} {chair_on} {neighbors_on}')
		if chair_on and neighbors_on >= 5:
			stable = False
			next_step[chair] = False
		elif not chair_on and neighbors_on == 0:
			stable = False
			next_step[chair] = True
		else:
			next_step[chair] = chair_on
	return next_step, stable

def find_stable_2(filename):
	chairs, maxx, maxy = get_floor(filename)
	# print_map(chairs, maxx+1, maxy+1)
	stable = False
	while not stable:
		chairs, stable = evolve2(chairs, maxx, maxy)
		# print_map(chairs, maxx+1, maxy+1)
	print(len(list(filter(lambda on: on, chairs.values()))))

find_stable_2('11.txt')