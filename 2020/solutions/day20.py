def rotate_point_counterclockwise(p, m):
	x, y = p
	return (y, m-x-1)

def rotate_point_clockwise(p, m):
	x, y = p
	return (m-y-1, x)

def flip_point(p, m):
	x, y = p
	return (m-1) - x, y

class Tile:
	def __init__(self, tile_id, pixels, m):
		self.tile_id = tile_id
		self.pixels = pixels
		self.m = m
		self.parse_edges()
	
	def parse_edges(self):
		# (top, right, down, left)
		# ten spaces, read ltr or utd so t/b l/r match
		top_edge, bottom_edge, left_edge, right_edge = self.get_edges()
		top = self.get_edge(top_edge)
		right = self.get_edge(right_edge)
		down = self.get_edge(bottom_edge)
		left = self.get_edge(left_edge)

		reversed_top = ''.join(reversed(top))
		reversed_right = ''.join(reversed(right))
		reversed_down = ''.join(reversed(down))
		reversed_left = ''.join(reversed(left))

		"""
		     | 0       | 90       | 180       | 270
		------------------------------------------------
		hv   | urdl    | LuRd     | DLUR      | rDlU
		hV   | UlDr    | RULD     | dRuL      | ldru
		Hv   | dRuL    | ldru     | UlDr      | RULD
		HV   | DLUR    | rDlU     | urdl      | LuRd
		-------------------------------------------------
		"""

		def reverse_permutation(p):
			return (p[3], p[2], p[1], p[0])

		permutations = [
			(top, right, down, left),
			(reversed_left, top, reversed_right, down),
			(reversed_down, reversed_left, reversed_top, reversed_right),
			(right, reversed_down, left, reversed_top),
		]
		permutations.append(reverse_permutation(permutations[3]))
		permutations.append(reverse_permutation(permutations[2]))
		permutations.append(reverse_permutation(permutations[1]))
		permutations.append(reverse_permutation(permutations[0]))
		self.permutations = permutations
		
	def get_edges(self):
		"top bottom left right"
		return (
			[(x, 0) for x in range(self.m)],
			[(x, self.m - 1) for x in range(self.m)],
			[(0, y) for y in range(self.m)],
			[(self.m - 1, y) for y in range(self.m)]
		)

	def get_edge(self, edge):
		return ''.join("#" if p in self.pixels else '.' for p in edge)

	def does_edge_match(top=None, bottom=None, left=None, right=None):
		assert any([top, bottom, left, right])
		perms = self.get_permutations()
	
	def get_permuted_set(self, perm):
		permuted_set = set()
		for p in self.pixels:
			pp = self.convert_coord(p, perm)
			permuted_set.add(pp)
		return permuted_set

	def convert_coord(self, p, perm):
		rotations = perm % 4
		flip = perm > 3
		result = p
		if flip:
			result = flip_point(result, self.m)
		for _ in range(rotations):
			result = rotate_point_clockwise(result, self.m)
		return result

	def bigset(self, perm, x_offset, y_offset):
		on_edge = lambda p: p[0] in (0, self.m - 1) or p[1] in (0, self.m - 1)
		bigset = set()
		for point in self.pixels:
			if on_edge(point):
				continue
			perm_p = self.convert_coord(point, perm) 
			full_grid_p = (
				perm_p[0] + (self.m * x_offset),
				perm_p[1] + (self.m * y_offset)
			)
			no_edge_p = (
				full_grid_p[0] - (1 + (2 * x_offset)),
				full_grid_p[1] - (1 + (2 * y_offset))
			)
			bigset.add(no_edge_p)
		return bigset

"""
7: 0
6: 1
5: 2
4: 3
3: 4
2: 5
1: 6
0: 7

2: 0
1: 1
0: 2



00 01 02 03 | 04 05 06 07
10 11 12 13 | 14 15 16 17
20 21 22 23 | 24 25 26 27
30 31 32 33 | 34 35 36 37
------------+-------------
40 41 42 43 | 44 45 46 47
50 51 52 53 | 54 55 56 57
60 61 62 63 | 64 65 66 67
70 71 72 73 | 74 75 76 77

11 12 15 16
21 22 25 26
51 52 55 56
61 62 65 66

00 01 02 03 04 05 06 07 08 09
10 11 12 13 14 15 16 17 18 19
20 21 22 23 24 25 26 27 28 29
30 31 32 33 34 35 36 37 38 39
40 41 42 43 44 45 46 47 48 49
50 51 52 53 54 55 56 57 58 59
60 61 62 63 64 65 66 67 68 60
70 71 72 73 74 75 76 77 78 79
80 81 82 83 84 85 86 87 88 89
90 91 92 93 94 95 96 97 98 99
"""

import re
tile_p = re.compile(r'Tile (?P<tile_id>\d*?):')

def make_tile(tile_lines):
	tile_id = tile_p.match(tile_lines[0]).group('tile_id')
	assert len(tile_id) > 0
	pixels = set()
	for y, tile_line in enumerate(tile_lines[1:]):
		for x, char in enumerate(tile_line):
			if char == '#':
				pixels.add((x, y))
	tile = Tile(tile_id, pixels, y + 1)
	return tile

def parse_tiles(filename):
	tiles = dict()
	buf = []
	for line in open('advent/input_files/'+ filename):
		line = line.strip()
		if line == '':
			tile = make_tile(buf)
			tiles[tile.tile_id] = tile
			buf = []
		else:
			buf.append(line)
	tile = make_tile(buf)
	tiles[tile.tile_id] = tile
	return tiles


from collections import namedtuple, deque
GameState = namedtuple("GameState", ['board', 'unplaced_tiles'])
PlacedTile = namedtuple("PlacedTile", ['tile_id', 'permutation'])
def get_tile(gamestate, p, m):
	if any(pi >= m or pi < 0 for pi in p):
		return None
	b = gamestate.board
	total_i = p[0] + (p[1] * m)
	try:
		return b[total_i]
	except:
		return None

def next_placeable_position(gamestate, m):
	for y in range(0, m):
		for x in range(0, m):
			if get_tile(gamestate, (x, y), m) is None:
				return (x, y)

def get_placeable_tiles(tiles, p, gamestate, m):
	# if len(gamestate.board) == 3 and gamestate.board[0].tile_id == '1951':
	# 	import pdb; pdb.set_trace()
	placeable_tiles = []
	x, y = p
	above = get_tile(gamestate, (x , y - 1), m)
	above_bottom = None
	if above:
		above_bottom = tiles[above.tile_id].permutations[above.permutation][2]

	left  = get_tile(gamestate, (x - 1, y), m)
	left_right = None
	if left:
		left_right = tiles[left.tile_id].permutations[left.permutation][1]
	
	def matches_edges(pt): 
		perm = tiles[pt.tile_id].permutations[pt.permutation]
		if above_bottom and above_bottom != perm[0]:
			return False
		if left_right and left_right != perm[3]:
			return False
		return True
	
	for unplaced_tile in gamestate.unplaced_tiles:
		for i in range(8):
			possible_pt = PlacedTile(unplaced_tile, i)
			if matches_edges(possible_pt):
				placeable_tiles.append(possible_pt)
	return placeable_tiles

def place_tile(gamestate, pt, p, m):
	unplaced_tiles = set(gamestate.unplaced_tiles)
	unplaced_tiles.remove(pt.tile_id)
	board = list(gamestate.board)
	board.append(pt),
	return GameState(board, unplaced_tiles)


# real_test_answer = [1951, 2311, 3079, 2729, 1427, 2473, 2971, 1489, 1171]
# def does_gs_match_answer(gs):
# 	# if gs.board[0] == 1951:
# 	# 	import pdb; pdb.set_trace()
# 	for i, tile in enumerate(gs.board):
# 		if str(real_test_answer[i]) != tile.tile_id:
# 			return False
# 	return True

from math import sqrt
def solve_tiles(filename):
	# import pdb; pdb.set_trace()
	tiles = parse_tiles(filename)
	all_tiles = list(tiles.keys())
	grid_size = int(sqrt(len(all_tiles)))
	assert len(all_tiles) % grid_size == 0
	state_queue = deque([GameState([], set(all_tiles))])
	done = False
	while not done:
		if not state_queue:
			print("no queue???")
		current_state = state_queue.popleft()
		next_position = next_placeable_position(current_state, grid_size)
		possible_placements = get_placeable_tiles(tiles, next_position, current_state, grid_size)
		if len(possible_placements) == 0:
			# print("no_possible states!")
			# print(current_state)
			continue
		for possible_placement in possible_placements:
			# print(possible_placement.tile_id)
			# if possible_placement.tile_id == "1951":
			# 	import pdb; pdb.set_trace()
			possible_state = place_tile(current_state, possible_placement, next_position, grid_size)
			if len(possible_state.unplaced_tiles) == 0:
				return possible_state, tiles
			state_queue.append(possible_state)

def mult_corners(gs):
	total_tiles = len(gs.board)
	m = int(sqrt(total_tiles))
	x = m -1
	corners = [
		(0, 0),
		(0, x),
		(x, 0),
		(x, x)
	]
	product = 1
	for corner in corners:
		product *= int(get_tile(gs, corner, m).tile_id)
	# print(product)


def generate_big_set(tiles, gs):
	big_set = set()
	m = int(sqrt(len(gs.board)))
	for i, tile in enumerate(gs.board):
		# import pdb; pdb.set_trace()
		y_offset = int(i / m)
		x_offset = i - (m * y_offset)
		# print(i, x_offset, y_offset)
		big_set.update(tiles[tile.tile_id].bigset(tile.permutation, x_offset, y_offset))
	return big_set

def print_set(icon_to_set, m, minv=0):
	for y in range(minv, m):
		line = ''
		for x in range(minv, m):
			p = (x, y)
			char = '.'
			for icon, s in icon_to_set.items():
				if p in s:
					char = icon
					break
			line += char
		print(line)
	print('\n')


dragon = [
	(0, 0),
	(1, 1),
	(4, 1),
	(5, 0),
	(6, 0),
	(7, 1),
	(10, 1),
	(11, 0),
	(12, 0),
	(13, 1),
	(16, 1),
	(17, 0),
	(18, -1),
	(18, 0),
	(19, 0)
]


def rotate_point_clockwise__graph(p):
	x, y = p
	return y, -x

def flip_point__graph(p):
	x, y = p
	return x, -y

def perm_dragon(perm):
		rotations = perm % 4
		flip = perm > 3
		result = dragon
		if flip:
			result = [flip_point__graph(p) for p in result]
		for _ in range(rotations):
			result = [rotate_point_clockwise__graph(p) for p in result]
		return result

dragon_perms = [perm_dragon(i) for i in range(8)]

def get_dragon_points_from_tailtip(p, perm):
	return [
		(p[0] + drag[0], p[1] + drag[1])
		for drag in dragon_perms[perm]
	]

# import pdb; pdb.set_trace()
# dragons = set()
# for i in range(8):
# 	dragons.update(perm_dragon(i))
# print_set(dragons, 20, -20)

def check_dragon(p, perm, pic):
	drag_points = get_dragon_points_from_tailtip(p, perm)
	for drag_point in drag_points:
		if drag_point not in pic:
			return False
	return True

def is_dragon(p, pic, perm=None):
	"""
	                  # 
	#    ##    ##    ### 
	 #  #  #  #  #  #    
	012345678901234567890123
	0         1         2
	"""
	if perm is not None:
		return check_dragon(p, perm, pic), perm
	for perm, pd in enumerate(dragon_perms):
		if check_dragon(p, perm, pic):
			return True, perm
	return False, None
		

def find_dragons(pic):
	perm = None
	dragon = set()
	for pixel in pic:
		d, p = is_dragon(pixel, pic, perm)
		if d:
			if perm is None:
				perm = p
			dragon_points = get_dragon_points_from_tailtip(pixel, perm)
			dragon.update(dragon_points)
	not_dragon = pic.difference(dragon)
	print_set({'O': dragon, '#': not_dragon}, 24)
	print(perm, len(not_dragon))

def do_part_2(filename):
	answer, tiles = solve_tiles(filename)

	big_set = generate_big_set(tiles, answer)
	print_set({"#": big_set}, 24)
	find_dragons(big_set)

do_part_2('20.txt')


# print_set(testtest_answer.board)

# for i in range(8):
# 	print('\n------------------------------\n')
# 	print(i)
# 	print_set(test_tiles['1951'].get_permuted_set(i), 10)

# real_answer = solve_tiles('20.txt')
# mult_corners(real_answer)
# print(real_answer.board)

""""
1951    2311    3079
2729    1427    2473
2971    1489    1171
"""