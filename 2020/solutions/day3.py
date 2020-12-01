from ..util import Point, Direction, move

class TreeMap:
	def __init__(self, filename):
		self.trees = set()
		with open('advent/input_files/'+filename, 'r') as f:
			for y, line in enumerate(f):
				y = -y
				for x, char in enumerate(line):
					if char == '#':
						self.trees.add(Point(x, y))
		self.x_size = x + 1
		self.y_size = -y + 1
	
	def check_position(self, p):
		normalized_p = Point(
			p.x % self.x_size,
			p.y
		)
		return normalized_p in self.trees

	def count_trees_from_angle(self, vector):
		current_point = Point(0, 0)
		trees = 0
		while abs(current_point.y) < self.y_size:
			if self.check_position(current_point):
				trees += 1
			current_point = move(current_point, vector)
		return trees

part_1_vector = Point(3, -1)

test_trees = TreeMap('3test.txt')
assert test_trees.count_trees_from_angle(part_1_vector) == 7

trees = TreeMap('3.txt')
print(trees.count_trees_from_angle(part_1_vector))

part_2_vectors = [
	Point(1, -1), part_1_vector, Point(5, -1), Point(7, -1), Point(1, -2)
]
def prod(iterator):
	product = 1
	for i in iterator:
		product *= i
	return product

part_2_ds = list(map(test_trees.count_trees_from_angle, part_2_vectors))
assert prod(part_2_ds) == 336

print(prod(map(trees.count_trees_from_angle, part_2_vectors)))