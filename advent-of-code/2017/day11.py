from .util import Point3D, HexDirection, hex_distance, move3d

f = open('advent2017/input_files/11.txt', 'r')
directions = f.readline().split(',')

def parse_hexdirection(d):
	if d == "n":
		return HexDirection.N
	elif d == "s":
		return HexDirection.S
	elif d == "ne":
		return HexDirection.NE
	elif d == "nw":
		return HexDirection.NW
	elif d == "se":
		return HexDirection.SE
	elif d == "sw":
		return HexDirection.SW

def hexmove(point, directions):
	current_point = point
	furthest_away = float('-inf')
	for direction in directions:
		direction = parse_hexdirection(direction)
		current_point = move3d(current_point, direction)
		current_distance = hex_distance(point, current_point)
		if current_distance > furthest_away:
			furthest_away = current_distance
			print(current_distance)
	return current_point, furthest_away

start_point = Point3D(0, 0, 0)
end_point, _ = hexmove(start_point, ['ne','ne','ne'])
assert hex_distance(end_point, start_point) == 3
end_point, _ = hexmove(start_point, ['ne','ne','sw','sw'])
assert hex_distance(end_point, start_point) == 0
end_point, _ = hexmove(start_point, ['ne','ne','s','s'])
assert hex_distance(end_point, start_point) == 2
end_point, _ = hexmove(start_point, ['se','sw','se','sw','sw'])
assert hex_distance(end_point, start_point) == 3

end_point, furthest = hexmove(start_point, directions)
print(hex_distance(end_point, start_point))
print(furthest)


	


