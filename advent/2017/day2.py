f = open("advent2017/input_files/02.txt", "r")
vals = [[int(a) for a in line.split('\t')] for line in f]

checksum = 0
for row in vals:
	checksum += max(row) - min(row)

print(checksum)

checksum = 0
from itertools import combinations
for row in vals:
	for a, b in combinations(row, 2):
		if a % b == 0:
			checksum += int(a/b)
			break
		elif b % a == 0:
			checksum += int(b/a)
			break

print(checksum)