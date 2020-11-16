GEN_A_START = 699
GEN_B_START = 124

GEN_A_F = 16807
GEN_B_F = 48271
GEN_DIVISOR = 2147483647

def generator(starting_val, factor):
	previous_val = starting_val
	while True:
		current_val = (previous_val * factor) % GEN_DIVISOR
		yield current_val
		previous_val = current_val

def generatorA(starting_val):
	return generator(starting_val, GEN_A_F)

def generatorB(starting_val):
	return generator(starting_val, GEN_B_F)

gen_a_test_res = [1092455, 1181022009, 245556042, 1744312007, 1352636452]
gen_b_test_res = [430625591, 1233683848, 1431495498, 137874439, 285222916]
gen_a_test = generatorA(65)
gen_b_test = generatorB(8921)

for a in gen_a_test_res:
	assert a == next(gen_a_test)

for b in gen_b_test_res:
	assert b == next(gen_b_test)

		
def judge(a, b):
	return a & 0xffff == b & 0xffff

judge_test = [False, False, True, False, False]
for i, expected in enumerate(judge_test):
	assert expected == judge(gen_a_test_res[i], gen_b_test_res[i])

ga = generatorA(GEN_A_START)
gb = generatorB(GEN_B_START)
#score = 0
#for i in range(40_000_000):
#	if judge(next(ga), next(gb)):
#		score += 1
#	if (i+1) % 1_000_000 == 0:
#		print((i+1) / 1_000_000)
#print(score)

def gen2(gen, n):
	while True:
		c = next(gen)
		while c % n != 0:
			c = next(gen)
		yield c

ga2 = gen2(ga, 4)
gb2 = gen2(gb, 8)

score = 0
for i in range(5_000_000):
	if judge(next(ga2), next(gb2)):
		score += 1
	if (i+1) % 1_000_000 == 0:
		print((i+1) / 1_000_000)
print(score)



