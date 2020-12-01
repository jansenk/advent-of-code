mask_36 = '0000000000000000000000000'
mask_36 = 34359738368

def get_value(mask_0, mask_1, value):
	"""
	mask 0 is a number that in binary represents the mask for zeroes.
	mask 1 is a number that in binary represents the mask for ones.
	"""
	value = value & (~mask_0)  # flip ones and zeroes, so anywhere that has a one, will result in a zero 
	value = value | mask_1  # anywhere with a one will leave a one
	return value 

def parse_mask(val):
	zero_mask = 0
	one_mask = 0
	for char in val:
		zero_mask = zero_mask << 1
		one_mask = one_mask << 1
		if char == '1':
			one_mask += 1
		if char == '0':
			zero_mask += 1
	return zero_mask, one_mask

def test_masking(mask, in_v, out_v):
	masks = parse_mask(mask)
	try:
		val = get_value(masks[0], masks[1], in_v)
		assert val == out_v
	except AssertionError:
		print(val)
		raise

tm = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'
test_masking(tm, 11, 73)
test_masking(tm, 101, 101)
test_masking(tm, 0, 64)

import re
mem_pattern = re.compile(r'mem\[(\d*?)\]')
def calc(filename):
	memory = dict()
	mask_0, mask_1 = 0, 0
	for line in open('advent/input_files/'+filename):
		target, _, value = line.split()
		if target == 'mask':
			mask_0, mask_1 = parse_mask(value)
		else:
			mem_address = int(mem_pattern.match(target).group(1))
			memory[mem_address] = get_value(mask_0, mask_1, int(value))
	print(sum(memory.values()))

calc('14.txt')

def parse_masks_2(val):
	mask = 0
	x_bits = []
	for i, char in enumerate(val):
		# print(bin(mask))
		mask = mask << 1
		if char == '1':
			mask += 1
		if char == 'X':
			x_bits.append(35 - i)
	# print(bin(mask))
	return mask, x_bits

def all_addresses(base, bits, i):
	bit = (1 << bits[i])
	off_ver = base & (~bit)
	on_ver = base | bit
	if i == len(bits) - 1:
		return [on_ver, off_ver]
	else:
		on_masks = all_addresses(on_ver, bits, i+1)
		off_masks = all_addresses(off_ver, bits, i+1)
		return on_masks + off_masks

def apply_masks_to_mem_address(mask, x_bits, mem_address):
	base_result = mem_address | mask
	for address in all_addresses(base_result, x_bits, 0):
		yield address

# print(list(map(bin, parse_all_masks('00000000000000000000000000000000X0XX'))))
def calc2(filename):
	memory = dict()
	mask, x_bits = 0, []
	for line in open('advent/input_files/'+filename):
		target, _, value = line.split()
		if target == 'mask':
			mask, x_bits = parse_masks_2(value)
		else:
			mem_address = int(mem_pattern.match(target).group(1))
			value = int(value)
			for mem_address_x in apply_masks_to_mem_address(mask, x_bits, mem_address):
				# print(f"writing {value} to {mem_address_x}/{bin(mem_address_x)}")
				memory[mem_address_x] = value
	print(sum(memory.values()))

calc2('14.txt')


