def find_differences(filename):
	with open('advent/input_files/'+filename) as f:
		numlist = sorted(map(int, f))
		# print(numlist)
		prevNum = 0
		differences = []
		for n in numlist:
			d = n - prevNum
			differences.append(d)
			prevNum = n
		differences.append(3)
		return differences

def find_ones_threes(filename):
	differences = find_differences(filename)
	ones = sum(1 for i in differences if i == 1)
	threes = sum(1 for i in differences if i == 3)
	print(f'{ones}, {threes}, {ones * threes}')

find_ones_threes('10.1.txt')
find_ones_threes('10.2.txt')
find_ones_threes('10.txt')


def find_configs(filename): 
	with open('advent/input_files/'+filename) as f:
		adapters = set(map(int, f))
	total_configs_for_input_joltage = dict()
	highest_joltage = max(adapters)
	def get_total_configs_for_input_joltage(j):
		nonlocal total_configs_for_input_joltage
		if j > highest_joltage:
			return 0
		if j == highest_joltage:
			return 1
		if j not in total_configs_for_input_joltage:
			total_configs = 0
			for jX in (j + 1, j+ 2, j + 3):
				if jX in adapters:
					total_configs += get_total_configs_for_input_joltage(jX)
			total_configs_for_input_joltage[j] = total_configs
		return total_configs_for_input_joltage[j]
	for i in reversed(range(highest_joltage + 1)):
		get_total_configs_for_input_joltage(i)
	print(total_configs_for_input_joltage[0])

find_configs('10.1.txt')
find_configs('10.2.txt')
find_configs('10.txt')

