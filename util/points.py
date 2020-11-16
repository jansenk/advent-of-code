from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
Point3D = namedtuple("Point3D", ["x", "y", "z"])

def move(p1, p2):
	return Point(
		p1.x + p2.x,
		p1.y + p2.y,
	)
	
def move3d(p1, p2):
	return Point3D(
		p1.x + p2.x,
		p1.y + p2.y,
		p1.z + p2.z
	)

def manhattan_distance(p1, p2):
	return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def hex_distance(p1, p2):
	return (abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)) / 2

class Direction:
	UP = Point(0, 1)
	DOWN = Point(0, -1)
	LEFT = Point(-1, 0)
	RIGHT = Point(1, 0)

	UR = move(UP, RIGHT)
	UL = move(UP, LEFT)
	DR = move(DOWN, RIGHT)
	DL = move(DOWN, LEFT)

	ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UR, UL, DR, DL]
	CARDINAL = [UP, DOWN, LEFT, RIGHT]

def surrounding_points(p):
	return [move(d, p) for d in Direction.ALL_DIRECTIONS]

def cardinal_surrounding_points(p):
	return [move(d, p) for d in Direction.CARDINAL]


class HexDirection:
	N = Point3D(0, 1, -1)
	S = Point3D(0, -1, 1)
	NE = Point3D(1, 0, -1)
	SE = Point3D(1, -1, 0)
	NW = Point3D(-1, 1, 0)
	SW = Point3D(-1, 0, 1)

