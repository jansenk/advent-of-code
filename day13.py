f = open('advent2017/input_files/13.txt', 'r')

scanners = {int(tokens[0]): int(tokens[1]) for tokens in map(lambda l: l.split(': '), f)}
highest = max(scanners.keys())

def is_scanner_tripped(step, size):
	return step % ((size - 1) * 2) == 0

severity = 0
for step, size in scanners.items():
	if is_scanner_tripped(step, size):
		severity += step*size

print(severity)

delay = 1
while True:
	caught = False
	for step, size in scanners.items():
		if is_scanner_tripped(step + delay, size):
			caught = True
			break
	if caught:
		delay += 1
	else:
		print(delay)
		break
	


