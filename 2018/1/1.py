import sys
f = open("input.txt", "r")
result = 0
vals = [int(line) for line in f]
print("Q1:" + str(sum(vals)))


def checkSeen(result, seen):
	if result in seen:
		return result
	seen.add(result)
	return None
	
def findDup():
	seen = set([0])
	result = 0
	loops = 0
	while True: 
		print("loop " + str(loops))
		for line in vals:
			result = result + int(line)
			r = checkSeen(result, seen)
			if r is not None:
				return r
		loops = loops + 1
		
print("Q2:" + str(findDup()))
		
		