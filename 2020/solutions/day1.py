from ..util import InputReader, assertEqual

inputs = InputReader.file_reader('1.txt')
real_ints = set(inputs.ints())

inputs = InputReader.file_reader('1-test.txt')
test_ints = set(inputs.ints())

def find_sum(inputs, target_sum):
	for i in inputs:
		j = target_sum - i
		if j in inputs:
			return i, j

assertEqual(find_sum(test_ints, 2020), (299, 1721))
i, j = find_sum(real_ints, 2020)
print(i * j)

def find_three_sum(inputs, target_sum):
	for i in inputs:
		inputs2 = set(inputs)
		inputs2.remove(i)
		remainder = target_sum - i
		result = find_sum(inputs2, remainder)
		if result:
			return i, result[0], result[1]

assertEqual(find_three_sum(test_ints, 2020), (675, 979, 366))
i, j, k = find_three_sum(real_ints, 2020)
print(i * j * k)
