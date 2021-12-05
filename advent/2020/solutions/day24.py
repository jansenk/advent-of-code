from ..util import Point3D, move3d, HexDirection

def directions(line):
	line = line.strip()
	i = 0
	while i < len(line):
		c = line[i]
		d = None
		skip = False
		if c == 'e':
			d = HexDirection.SE
		elif c == 'w':
			d = HexDirection.NW
		else:
			skip = True
			c = line[i:i+2]
			if c == 'nw':
				d = HexDirection.N
			elif c == 'ne':
				d = HexDirection.NE
			elif c == 'sw':
				d = HexDirection.SW
			elif c == 'se':
				d = HexDirection.S
		i += 2 if skip else 1
		yield d

def flip_tiles(filename):
	f = open('advent/input_files/'+filename)
	black_tiles = set()
	starting_tile = Point3D(0, 0, 0)
	for line in f:
		line = line.strip()
		tile = starting_tile
		direction_g = directions(line)
		for d in direction_g:
			tile = move3d(tile, d)
		if tile in black_tiles:
			black_tiles.remove(tile)
		else:
			black_tiles.add(tile)
	print(len(black_tiles))
	return black_tiles

flip_tiles('24.txt')

def get_neighbors(tile):
	return [move3d(tile, d) for d in HexDirection.ALL_DIRECTIONS]

def num_neighbors(tile, black_tiles):
	neighbors = 0
	for d in HexDirection.ALL_DIRECTIONS:
		neighbor_tile = move3d(tile, d)
		if neighbor_tile in black_tiles:
			neighbors += 1
	return neighbors

# def max_coords(black_tiles):
# 	xmin, xmax = (float('inf'), float('-inf'))
# 	ymin, ymax = (float('inf'), float('-inf'))
# 	zmin, zmax = (float('inf'), float('-inf'))
# 	for tile in black_tiles:
# 		if tile.x < xmin:
# 			xmin = tile.x
# 		elif tile.x > xmax:
# 			xmax = tile.x

# 		if tile.y < ymin:
# 			ymin = tile.y
# 		elif tile.y > ymax:
# 			ymax = tile.y

# 		if tile.z < zmin:
# 			zmin = tile.z
# 		elif tile.z > zmax:
# 			zmax = tile.z

# 	return (xmin, xmax, ymin, ymax, zmin, zmax)

def floor_of_life(black_tiles):
	new_black = set()
	checked_white_neighbors = set()
	# xmin, xmax, ymin, ymax, zmin, zmax = max_coords(black_tiles)
	for tile in black_tiles:
		neighbors = get_neighbors(tile)
		assert len(neighbors) == 6
		white_neighbors = [n for n in neighbors if n not in black_tiles]
		black_neighbors = 6 - len(white_neighbors)

		if black_neighbors == 0 or black_neighbors > 2:
			# turn off, not added to new set
			pass
		else:
			new_black.add(tile)
		
		for neighbor in white_neighbors:
			if neighbor in checked_white_neighbors:
				continue
			checked_white_neighbors.add(neighbor)
			num_black_neighbors = num_neighbors(neighbor, black_tiles)
			if num_black_neighbors == 2:
				new_black.add(neighbor)
	return new_black

def solve_p2(filename):
	current_tiles = flip_tiles(filename)
	for i in range(100):
		current_tiles = floor_of_life(current_tiles)
		print(f"Day {i+1}: {len(current_tiles)}")

solve_p2('24.txt')

