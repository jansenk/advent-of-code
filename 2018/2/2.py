f = open("in.txt", 'r')
boxes = [l.strip() for l in f]


def parse_box(box):
    letters = dict()
    for letter in box:
        count = 1
        if letter in letters:
            count = letters[letter] + 1
        letters[letter] = count
    twice = []
    thrice = []
    for (letter, count) in letters.iteritems():
        if count == 2:
            twice.append(letter)
        elif count == 3:
            thrice.append(letter)
    return letters, twice, thrice


two = three = 0
for box in boxes:
    parsed_box = parse_box(box)
    if parsed_box[1]:
        two = two+1
    if parsed_box[2]:
        three = three+1

print "%d * %d = %d" % (two, three, two * three)


def find_duplicate_modified_tag():
    for i in range(0, len(boxes[0])):
        results = set()
        print("Character %d" % i)
        for box in boxes:
            first_half = box[:i]
            second_half = box[i+1:]
            modified = first_half + second_half
            if modified in results:
                return modified
            results.add(modified)
        print("No dupes found for character %d" % i)
    print("Something went wrong!")


result = find_duplicate_modified_tag()
print("Result: %s" % result)






