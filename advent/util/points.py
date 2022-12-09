from math import sqrt
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
Point3D = namedtuple("Point3D", ["x", "y", "z"])

def move(p1, p2):
	return Point(
		p1.x + p2.x,
		p1.y + p2.y,
	)

def moven(p, d, n):
	return move(
		Point(d.x * n, d.y * n),
		p
	)

def recenter(p0, p1):
	return Point(p1.x - p0.x, p1.y - p0.y)

def move3d(p1, p2):
	return Point3D(
		p1.x + p2.x,
		p1.y + p2.y,
		p1.z + p2.z
	)

def manhattan_distance(p1, p2):
	return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def chebshayev_distance(p1, p2):
    return max(abs(p1.x - p2.x), abs(p1.y - p2.y))

def manhattan_distance_3d(p1, p2):
	return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)

def hex_distance(p1, p2):
	return (abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)) / 2

def apply3d(p, f):
	return Point3D(
		f(p.x),
		f(p.y),
		f(p.z)
	)
 
def vector(p1, p2):
    """ Bad name. If I a at p1, what vector do I need to get to p2?"""
    return Point(
		p2.x - p1.x,
		p2.y - p1.y,
	)

def _ordinality(n):
		if n == 0:
			return 0
		if n > 0:
			return 1
		if n < 0:
			return -1

def unit_vector(v):
    return Point(
		_ordinality(v.x),
		_ordinality(v.y),
	)

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

	@staticmethod
	def reverse(direction):
		if direction == Direction.UP:
			return Direction.DOWN
		if direction == Direction.DOWN:
			return Direction.UP
		if direction == Direction.LEFT:
			return Direction.RIGHT
		if direction == Direction.RIGHT:
			return Direction.LEFT
		raise NotImplementedError()

	_clockwise_cardinal = [UP, RIGHT, DOWN, LEFT]
	@staticmethod
	def rotate_cardinal(direction, clockwise_steps):
		start = Direction._clockwise_cardinal.index(direction)
		return Direction._clockwise_cardinal[(start + clockwise_steps) % 4]
	
	@staticmethod
	def name(d):
		if d == Direction.UP:
			return 'UP'
		if d == Direction.DOWN:
			return 'DOWN'
		if d == Direction.LEFT:
			return 'LEFT'
		if d == Direction.RIGHT:
			return 'RIGHT'

	@staticmethod
	def parse(s):
		s = s.lower()
		if s in ('up', 'u', 'north', 'n'):
			return Direction.UP
		if s in ('down', 'd', 'south', 's'):
			return Direction.DOWN
		if s in ('left', 'l', 'west', 'w'):
			return Direction.LEFT
		if s in ('right', 'r', 'east', 'e'):
			return Direction.RIGHT

def surrounding_points(p):
	return [move(d, p) for d in Direction.ALL_DIRECTIONS]

def cardinal_surrounding_points(p):
	return [move(d, p) for d in Direction.CARDINAL]


class HexDirection:
	"""
	This is for a grid with a 'flat' top hex.
	For a 'pointy' top, just rotate all directions one 'tick'
	counterclockwise
	"""
	N = Point3D(0, 1, -1)
	S = Point3D(0, -1, 1)
	NE = Point3D(1, 0, -1)
	SE = Point3D(1, -1, 0)
	NW = Point3D(-1, 1, 0)
	SW = Point3D(-1, 0, 1)
	ALL_DIRECTIONS = [N, S, NE, SE, NW, SW]
