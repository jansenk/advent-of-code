f = open('advent2017/input_files/09.txt', 'r')

total_score = 0
current_score = 0
garbage_chars = 0
currently_garbage = False
ignore_char = False
while True:
	c = f.read(1)
	if not c:
		break

	if ignore_char:
		ignore_char = False
	elif c == "!":
		ignore_char = True
	elif c == ">":
		currently_garbage = False
	elif currently_garbage:
		garbage_chars += 1
	elif c == "<":
		currently_garbage = True
	elif c == "{":
		current_score += 1
	elif c == "}":
		total_score += current_score
		current_score -= 1

print(total_score)
print(garbage_chars)