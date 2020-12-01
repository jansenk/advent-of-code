class Cup:
	def __init__(self, cup_id):
		self.cup_id = cup_id
		self.next_cup = None
	def __repr__(self):
		return f"{self.cup_id} -> {self.next_cup.cup_id}"

def parse_cup_circle(s):
	cups = dict()
	first_cup = None
	prev_cup = None
	for c in s:
		cup_id = int(c)
		cup = Cup(cup_id)
		cups[cup_id] = cup
		if first_cup is None:
			first_cup = cup
		elif prev_cup is not None:
			prev_cup.next_cup = cup
		prev_cup = cup
	prev_cup.next_cup = first_cup
	return cups, first_cup

def do_a_step(current_cup, cups):
	# print("current cup: "+ str(current_cup.cup_id))
	first_cup = current_cup.next_cup
	second_cup = first_cup.next_cup
	third_cup = second_cup.next_cup
	fourth_cup = third_cup.next_cup
	removed_cups = {first_cup.cup_id, second_cup.cup_id, third_cup.cup_id}
	# print("pick up: " + str(removed_cups))

	third_cup.next_cup = None
	current_cup.next_cup = fourth_cup

	destination_cup_id = current_cup.cup_id - 1
	destination_cup = None
	while destination_cup is None:
		if destination_cup_id == 0:
			destination_cup_id = 9
		if destination_cup_id in removed_cups:
			destination_cup_id -= 1
		else:
			 destination_cup = cups[destination_cup_id]
	
	# print("destination cup: " + str(destination_cup_id))
	destination_next_cup = destination_cup.next_cup
	destination_cup.next_cup = first_cup
	third_cup.next_cup = destination_next_cup

	return current_cup.next_cup

def print_loop(starting_cup):
	current_cup = starting_cup.next_cup
	result = ""
	while current_cup is not starting_cup:
		result += str(current_cup.cup_id)
		current_cup = current_cup.next_cup
	return result

def solve_p1(s):
	cups, current_cup = parse_cup_circle(s)
	for i in range(100):
		current_cup = do_a_step(current_cup, cups)
	print(print_loop(cups[1]))

solve_p1('389125467')
solve_p1('326519478')

"[] array: index:value index=Cup_id, value= next"
def solve_p2(s):
	cups, current_cup = parse_cup_circle(s)
	a = [i+1 for i in range(1_000_000 + 1)]
	a[0] = None
	a[-1] = current_cup.cup_id
	for i in range(1, 10):
		next_cup = cups[i].next_cup.cup_id
		if next_cup == current_cup.cup_id:
			a[i] = 10
		else:
			a[i] = next_cup

	def do_a_step_array_1(cc):
		first_cup = a[cc]
		second_cup = a[first_cup]
		third_cup = a[second_cup]
		fourth_cup = a[third_cup]
		# print("pick up: " + str(removed_cups))

		# third_cup.next_cup = None
		# current_cup.next_cup = fourth_cup
		a[third_cup] = None
		a[cc] = fourth_cup

		# destination_cup_id = current_cup.cup_id - 1
		dc = cc
		while True:
			dc -= 1
			if dc == 0:
				dc = 1_000_000
			if dc != first_cup and dc != second_cup and dc != third_cup:
				break
		
		# print("destination cup: " + str(destination_cup_id))
		destination_next_cup = a[dc]
		a[dc] = first_cup
		a[third_cup] = destination_next_cup

		return fourth_cup
	current_cup = current_cup.cup_id
	for _ in range(10_000_000):
		current_cup = do_a_step_array_1(current_cup)
	a1 = a[1]
	aa1 = a[a1]
	print('------')
	print(a1)
	print(aa1)
	print(a1 * aa1)

solve_p2('389125467')
solve_p2('326519478')








