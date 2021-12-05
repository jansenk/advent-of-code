from ..util import InputReader, assertEqual
from collections import Counter

def is_password_valid(password, target, target_min, target_max):
		password_charcount = Counter(password)
		target_count = password_charcount[target]
		return target_count >= target_min and target_count <= target_max

def parse_line(line):
	numeric_range, target, password = line.split()
	target_min, target_max = map(int, numeric_range.split('-'))
	target = target[0]
	return password, target, target_min, target_max

inputs = InputReader.file_reader('2.txt')
parsed_passwords = list(map(parse_line, inputs.lines()))
inputs.close()
count = 0
print(len(list(filter(lambda p: is_password_valid(*p), parsed_passwords))))

def is_password_valid_2(password, target, i, j):
	is_i = password[i-1] == target
	is_j = password[j-1] == target
	return (is_i or is_j) and not (is_i and is_j) # how tf xor in python lmao

print(len(list(filter(lambda p: is_password_valid_2(*p), parsed_passwords))))

