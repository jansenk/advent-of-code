from collections import defaultdict
def game(starting_numbers, end_turn):
	memory = dict()
	turn = 1
	last_said_number = starting_numbers[0]
	for number in starting_numbers[1:]:
		turn += 1
		# print(f'turn {turn}, {number}')
		memory[last_said_number] = turn - 1
		last_said_number = number
	# print(memory)
	while turn < end_turn:
		turn += 1
		last_said_number = number
		if last_said_number in memory:
			last_said_turn = memory[last_said_number]
			number = turn - last_said_turn - 1
		else:
			number = 0
		memory[last_said_number] = turn - 1
	return number

# assert game([0, 3, 6], 2020) == 436
# assert game([1, 3, 2], 2020) == 1
# assert game([2, 1, 3], 2020) == 10
# assert game([1, 2, 3], 2020) == 27
# assert game([2, 3, 1], 2020) == 78
# assert game([3, 2, 1], 2020) == 438
# assert game([3, 1, 2], 2020) == 1836

print(game([10,16,6,0,1,17], 2020))
print(game([10,16,6,0,1,17], 30000000))