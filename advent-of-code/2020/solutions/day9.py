def is_sum_in_set(i, s):
	for j in s:
		remainder = i - j
		if remainder < 0:
			continue
		if remainder in s.difference({j}):
			return True
	return False

from collections import deque
def find_non_sum(filename, buf_size):
	with open('advent/input_files/'+filename) as f:
		buf = deque()
		for i in map(int, f):
			if len(buf) < buf_size:
				buf.append(i)
			else:
				# import pdb; pdb.set_trace()
				if not is_sum_in_set(i, set(buf)):
					print(i)
					return
				else:
					buf.popleft()
					buf.append(i)

# find_non_sum('9.1.txt', 5)
find_non_sum('9.txt', 25)


class AdditionSegment:
	def __init__(self, i, val):
		self.i = i
		self.j = i
		self.val = val
	
	def expand(self, j):
		self.j += 1
		self.val += j
	
	def get_soln(self, vals):
		seg = vals[self.i:self.j+1]
		return min(seg) + max(seg)

def find_sum_chain(filename, target):
	with open('advent/input_files/'+filename) as f:
		inputs = list(map(int, f))
	segments = []
	for i in range(len(inputs)):
		for segment in segments:
			segment.expand(inputs[i])
			if segment.val == target:
				print(segment.get_soln(inputs))
				return
		segments.append(AdditionSegment(i, inputs[i]))
		segments = [segment for segment in segments if segment.val < target]

# find_sum_chain('9.1.txt', 127)
find_sum_chain('9ZX.txt', 167829540)

# """
# 1, 2, 3, 4, 5
# 1+2 1+3 1+4 1+5
#     2+3 2+4 2+5
#         3+4 3+5
#             4+5

#   2   3   4   5  6
# X1+2 1+3 1+4 1+5X
#     2+3 2+4 2+5 2+6
#         3+4 3+5 3+6
#             4+5 4+6
#                 5+6

# """

# class RunningSums:
# 	def __init__(self, size, buffer):
# 		self.size = size
# 		self.sum_rows = [[] for _ in range(size)]
# 		self.load_buffer(buffer)
	
# 	def load_buffer(self, buffer):
# 		for i in range(len(buffer)):
# 			sum_row = 
# 			for j in range(i+1, len(buffer)):
# 				s = buffer[i] + buffer[j]

	
# 	def add()