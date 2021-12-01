from .util import WrapAroundIterator, WrapAroundList

f = open("advent2017/input_files/01.txt", "r")
vals = [int(digit) for digit in [line for line in f][0]]

total = 0
for val, nextval in WrapAroundIterator(vals):
	if val == nextval:
		total = total + val

print(total)

wraparound = WrapAroundList(vals)
l = len(vals)
step = int(l/2)
total = 0
for i, val in enumerate(vals):
	if val == wraparound[i+step]:
		total += val
print(total)

