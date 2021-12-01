f = open('advent2017/input_files/10.txt', 'r')
line = f.readline()

def knot_hash(lengths, string_len=256, loops=1):
	string = [i for i in range(string_len)]
	
	def simple_flip(current_index, ending_index):
		nonlocal string
		if ending_index == len(string) - 1:
			ending_index = None
		else:
			ending_index += 1
		string[current_index:ending_index] = reversed(string[current_index:ending_index])

	def complicated_flip(current_index, ending_index, length):
		nonlocal string
		first_bit = string[current_index:]
		first_bit_len = len(first_bit)
		remaining_len = length - first_bit_len
		second_bit = string[:remaining_len]
		full_str = list(reversed(first_bit + second_bit))
		string[current_index:] = full_str[:first_bit_len]
		string[:remaining_len] = full_str[first_bit_len:]

	current_index = 0
	current_skip = 0
	for _ in range(loops):
		for length in lengths:
			ending_index = current_index + length - 1
			if ending_index <= len(string) - 1:
				simple_flip(current_index, ending_index)
			else:
				complicated_flip(current_index, ending_index, length)
			current_index = (current_index + length + current_skip) % len(string)
			current_skip += 1
	return string

l1 = [int(i) for i in line.split(',')]
s1 = knot_hash(l1)
print(s1[0]*s1[1])

def string_to_ascii_list(s):
	return [ord(c) for c in s]
assert string_to_ascii_list('1,2,3') == [49,44,50,44,51]

def make_dense(a):
	i = 0
	result = []
	while i < len(a):
		current_hash = a[i]
		for j in range(1, 16):
			current_hash = current_hash ^ a[i+j]
		result.append(current_hash)
		i += 16
	return result
dt = make_dense([65, 27, 9, 1, 4, 3, 40, 50, 91, 7, 6, 0, 2, 5, 68, 22])
assert dt == [64]

def hex_str(l):
	xl = ["{:02x}".format(a) for a in l]
	return ''.join(xl)
assert hex_str([64, 7, 255]) == '4007ff'

def knot_hash_from_string(s):
	suffix = [17, 31, 73, 47, 23]
	lengths = string_to_ascii_list(s) + suffix
	string = knot_hash(lengths, loops=64)
	dense = make_dense(string)
	return hex_str(dense)

assert knot_hash_from_string('') == 'a2582a3a0e66e6e86e3812dcb672a272'
assert knot_hash_from_string('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
assert knot_hash_from_string('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
assert knot_hash_from_string('1,2,4') ==  '63960835bcdc130f0b66d7ff4f6a5a8e'

print(knot_hash_from_string(line))
