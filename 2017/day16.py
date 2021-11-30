from collections import deque
ord_a = ord('a')
dancers = 'abcdefghijklmnop'

with open('advent2017/input_files/16.txt', 'r') as f:
	line = f.readline()
	instructions = line.split(',')

def find_indexes(dancers, a, b):
	ia = None
	ib = None
	for i, dancer in enumerate(dancers):
		if dancer == a:
			ia = i
		if dancer == b:
			ib = i
		if ia and ib:
			break
	return ia, ib
	
def dance(dancers, instructions, end_condition=None):
	if not end_condition:
		end_condition = lambda d, _: d == 1
	current_state = ''.join(dancers)
	dancers = deque(dancers)
	dances = 0
	while not end_condition(dances, current_state):
		for instruction in instructions:
			if instruction[0] == 's':
				spins = int(instruction[1:])
				dancers.rotate(spins)
			elif instruction[0] == 'x':
				a, b = instruction[1:].split('/')
				a, b = int(a), int(b)
				t = dancers[a]
				dancers[a] = dancers[b]
				dancers[b] = t
			elif instruction[0] == 'p':
				a, b = instruction[1:].split('/')
				ia, ib = find_indexes(dancers, a, b)
				t = dancers[ia]
				dancers[ia] = dancers[ib]
				dancers[ib] = t
		current_state = ''.join(dancers)
		dances += 1
	return current_state, dances

assert dance('abcde', ['s1', 'x3/4', 'pe/b'])[0] == 'baedc'
print(dance(dancers, instructions))
startstate = str(dancers)
print(dance(dancers, instructions, end_condition=lambda d, cs: cs==startstate and d != 0))
print(dance(dancers, instructions, end_condition=lambda d, _: d==34))
