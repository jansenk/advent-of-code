TARGET = 361527

from math import sqrt, ceil, floor


"""
n x n grid - odd, so 1 is center
m x m grid, - even, should convert to nxn


side = m
edge = additional numbers added by adding next square.
5x5, 17 - 25 are edge

"""
min_corner_size = ceil(sqrt(TARGET))
max_grid_val = min_corner_size ** 2
top_left = max_grid_val % 2 == 0

if top_left:
	grid_size = min_corner_size + 1
else:
	grid_size = min_corner_size

grid_val = min_corner_size**2
previous_grid_val = (grid_size - 2)**2

outer_edge_min = previous_grid_val + 1

midpoint_1 = outer_edge_min + floor(grid_size/2) - 1
corner_1 = outer_edge_min + grid_size - 2

midpoint_2 = corner_1 + floor(grid_size/2)
corner_2 = corner_1 + grid_size - 1

midpoint_3 = corner_2 + floor(grid_size/2)
corner_3 = corner_2 + grid_size - 1

midpoint_4 = corner_3 + floor(grid_size/2)
corner_4 = corner_3 + grid_size - 1

midpoints = [midpoint_1, midpoint_2, midpoint_3, midpoint_4]

part_one = min(set(abs(TARGET - midpoint) for midpoint in midpoints))

part_two = floor(grid_size/2)

print(part_one+part_two)


from .util import Point, surrounding_points, Direction, move
grid = dict()

def get_grid_value(p):
	try:
		return grid[p]
	except:
		return 0

def grid_coordinate_generator(n):
	if n % 2 == 0:
		raise Exception("nah")
	
	middle = floor(n/2)
	
	current_point = Point(middle, middle)
	yield current_point
	
	max_val = n**n
	current_pval = 2
	current_root = 1
	while current_pval <= max_val:
		for direc, moves in [ 
			(Direction.RIGHT, current_root),
			(Direction.UP, current_root),
			(Direction.LEFT, current_root+1),
			(Direction.DOWN, current_root+1),
		]:
			for _ in range(moves):
				next_point = move(current_point, direc)
				yield next_point
				current_pval += 1
				current_point = next_point
		current_root += 2

coords = grid_coordinate_generator(grid_size)
first_point = next(coords)
current_grid_value = 1
grid[first_point] = 1
while current_grid_value <= TARGET:
	current_point = next(coords)
	surroundings = surrounding_points(current_point)
	current_grid_value = sum([get_grid_value(p) for p in surroundings])
	grid[current_point] = current_grid_value

print(current_grid_value)
	
	
	
	
	






