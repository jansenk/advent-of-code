import re
from math import floor
p = re.compile(r'([FB]{7})([LR]{3})')

def binary(input_str, current_min, current_max):
	for c in input_str:
		midpoint = (current_min + current_max) / 2
		bottom_mid = floor(midpoint)
		top_mid = bottom_mid + 1
		if c in ['F', 'L']:
			current_max = bottom_mid
		else:
			current_min = top_mid
	assert current_max == current_min
	return current_min

assert binary('FBFBBFF', 0, 127) == 44
assert binary('RLR', 0, 7) == 5

def parse_seat(seat):
	m = p.match(seat)
	front_back, left_right = m.groups()
	row = binary(front_back, 0, 127)
	column = binary(left_right, 0, 7)
	return row, column

assert parse_seat('FBFBBFFRLR') == (44, 5)

def get_seat_id(parsed_seat):
	row, column = parsed_seat
	return (row * 8) + column

assert get_seat_id((44, 5)) == 357

def parse_seat_id(seat):
	return get_seat_id(parse_seat(seat))

assert parse_seat_id('FBFBBFFRLR') == 357
assert parse_seat_id('BFFFBBFRRR') == 567
assert parse_seat_id('FFFBBBFRRR') == 119
assert parse_seat_id('BBFFBBFRLL') == 820

highest_seat = float('-inf')
with open('advent/input_files/5.txt') as f:
	seats = [parse_seat_id(l) for l in f]
	max_seat = max(seats)
	print(max_seat)
	min_seat = min(seats)
	import pdb; pdb.set_trace()
	triangular = lambda i: int(((i + 1) * i) / 2)
	sum_seats = triangular(max_seat) - triangular(min_seat-1)
	print(sum_seats - sum(seats))
