f = open("advent2017/input_files/05.txt", "r")
original_program = [int(line) for line in f]
program = list(original_program)
max_pointer = len(program) - 1 
pointer = 0
count = 0
while pointer >=0 and pointer <= max_pointer:
	count += 1
	current_value = program[pointer]
	program[pointer] += 1
	pointer += current_value
print(count)

program = original_program
pointer = 0
count = 0
while pointer >=0 and pointer <= max_pointer:
	count += 1
	current_value = program[pointer]
	if current_value >= 3:
		program[pointer] -= 1
	else:
		program[pointer] += 1
	pointer += current_value

print(count)
