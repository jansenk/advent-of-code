
def parse_instructions(filename):
	instructions = []
	with open('advent/input_files/'+filename) as f:
		for line in f:
			code, value = line.split()
			value = int(value)
			instructions.append((code, value))
	return instructions

def calc(p, ip, acc, prnt=False):
	inc = True
	op, val = p[ip]
	if prnt:
		print(f'{ip}, {op}, {val}, {acc}')
	if op == 'acc':
		acc += val
	elif op == 'jmp':
		ip += val
		inc = False
	if inc:
		ip += 1
	return ip, acc

def find_loop(p, prnt):
	acc = 0
	ip = 0
	seen_ip = set()
	while ip not in seen_ip:
		seen_ip.add(ip)
		ip, acc = calc(p, ip, acc, prnt)
	return ip, acc, seen_ip


instructions = parse_instructions('8.1.txt')
assert find_loop(instructions, False)[1] == 5

instructions = parse_instructions('8.txt')
end_ip, end_acc, end_seen = find_loop(instructions, False)
print(end_acc)

def try_to_complete(instructions):
	ip = 0
	acc = 0
	seen_ip2 = set()
	while ip < len(instructions):
		if ip in seen_ip2:
			return False
		seen_ip2.add(ip)
		ip, acc = calc(instructions, ip, acc)
	return acc 

for ip in filter(lambda ip: instructions[ip][0] in ('jmp', 'nop'), end_seen):
	op, val = instructions[ip]
	if op == 'nop':
		new_op = 'jmp'
		new_ip = ip + val
	elif op == 'jmp':
		new_op = 'nop'
		new_ip = ip + 1
	else:
		continue

	if new_ip not in end_seen:
		new_inst = list(instructions)
		new_inst[ip] = (new_op, val)
		end = try_to_complete(new_inst)
		if end:
			print(end)
			raise StopIteration
