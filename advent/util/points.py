from collections import namedtuple
from dataclasses import dataclass

Point = namedtuple("Point", ["x", "y"])
@dataclass
class Vector:
	dx: int
	dy: int
 
	def __add__(self, v2):
		return Vector(self.dx + v2.dx, self.dy + v2.dy)
 
 
Point3D = namedtuple("Point3D", ["x", "y", "z"])
Vector3D = namedtuple("Vector3D", ["dx", "dy", "dz"])
    
def move(p, v):
	return Point(
		p.x + v.dx,
		p.y + v.dy,
	)

def moven(p, v, n):
	return move(
		Vector(v.dx * n, v.dy * n),
		p
	)

def _subtract(a, b):
    return (b.x - a.x, b.y - a.y)

def recenter(p0, p1):
	""" Returns a point with the coordinates of p1 if p0 was the origin """
	return Point(*_subtract(p0, p1))

def vector_to(p1, p2):
    """ If I a at p1, what vector do I need to get to p2?"""
    return Vector(*_subtract(p1, p2))

def move3d(p, v):
	return Point3D(
		p.x + v.dx,
		p.y + v.dy,
		p.z + v.dz
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
	UP = Vector(0, 1)
	DOWN = Vector(0, -1)
	LEFT = Vector(-1, 0)
	RIGHT = Vector(1, 0)

	UR = UP + RIGHT
	UL = UP + LEFT
	DR = DOWN + RIGHT
	DL = DOWN + LEFT

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
	return [move(p, d) for d in Direction.ALL_DIRECTIONS]

def cardinal_surrounding_points(p):
	return [move(p, d) for d in Direction.CARDINAL]


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
