from collections import defaultdict

registers = defaultdict(int)

f = open('advent2017/input_files/08.txt', 'r')
cond_op = {
	">": lambda x, y: x > y,
	"<": lambda x, y: x < y,
	"==": lambda x, y: x == y,
	">=": lambda x, y: x >= y,
	"<=": lambda x, y: x <= y,
	"!=": lambda x, y: x != y,
}

max_val = float('-inf')
for line in f:
	tokens = line.split()
	target_register, action, value = tokens[:3]
	cond_target_register, cond_action, cond_value = tokens[4:]
	value = int(value)
	cond_value = int(cond_value)
	if cond_op[cond_action](registers[cond_target_register], cond_value): 
		if action == 'dec':
			value *= -1
		registers[target_register] += value
		curr_max = max(registers.values())
		if curr_max > max_val:
			max_val = curr_max

print(max(registers.values()))
print(max_val)