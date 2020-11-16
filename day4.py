f = open("advent2017/input_files/04.txt", "r")
valid = 0
for line in f:
	words = line.split()
	wordset = set(words)
	if len(words) == len(wordset):
		valid += 1
print(valid)

f.seek(0)
valid_count = 0
for line in f:
	words = line.split()
	word_set = set()
	valid = True
	for word in words:
		alphabetized_word = ''.join(sorted(word))
		if alphabetized_word in word_set:
			valid = False
			break
		word_set.add(alphabetized_word)
	if valid:
		valid_count += 1
print(valid_count)
	