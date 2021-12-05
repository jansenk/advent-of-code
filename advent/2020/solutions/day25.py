def op(value, subject):
	value *= subject
	value %= 20201227
	return value

def transform(subject, loop):
	value = 1
	for _ in range(loop):
		value = op(value, subject)
	return value

def find_loop_size(pubkey):
	current_loop = 0
	current_value = 1
	while current_value != pubkey:
		current_value = op(current_value, 7)
		current_loop += 1
	return current_loop

# print(find_loop_size(17807724))
# print(transform(17807724, 8))
# print(transform(5764801, 11))

INPUT_KEYS = (16915772, 18447943)
card_loop_size = find_loop_size(INPUT_KEYS[0])
door_loop_size = find_loop_size(INPUT_KEYS[1])
print(transform(INPUT_KEYS[0], door_loop_size))