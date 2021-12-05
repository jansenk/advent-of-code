from .util import WrapAroundList

banks = [4,1,15,12,0,9,9,5,5,8,7,3,14,5,12,3]
#banks = [0,2,7,0]

def largest_index(banks):
	largest = float('-inf')
	largest_i = None
	for i in range(len(banks)):
		if banks[i] > largest:
			largest = banks[i]
			largest_i = i
	return largest_i

cycle_count = 0
block_records = {}
inf_loop = False
wrap_around_banks = WrapAroundList(banks)
while not inf_loop:
	cycle_count += 1
	selected_bank = largest_index(banks)
	selected_bank_blocks = banks[selected_bank]
	banks[selected_bank] = 0
	for i in range(selected_bank_blocks):
		wrap_around_banks[selected_bank+i+1] += 1
	block_state = str(banks)
	if block_state in block_records:
		break;
	block_records[block_state] = cycle_count

print(cycle_count)
print(cycle_count - block_records[str(banks)])