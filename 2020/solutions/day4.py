def parse_passports(filename):
	passports = []
	with open('advent/input_files/'+filename, 'r') as f:
		current_passport = dict()
		def passport_done():
			nonlocal passports
			nonlocal current_passport
			passports.append(current_passport)
			current_passport = dict()
		for line in f:
			if line == '\n':
				passport_done()
			else:
				passport_fields = line.split()
				for field in passport_fields:
					key, value = field.split(':')
					current_passport[key] = value
		passport_done()
	return passports

required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
srequired_fields = sorted(required_fields)

def is_valid(passport):
	passport_keys = set(passport.keys())
	# print('--------------------------')
	# print(sorted(passport_keys))
	# print(srequired_fields)
	ss = required_fields.issubset(passport_keys)
	# print(ss)
	return ss

test_passports = parse_passports('4-test.txt')
valid_count = sum(1 for _ in filter(is_valid, test_passports))
assert valid_count == 2 

real_passports = parse_passports('4.txt')
valid_count = sum(1 for _ in filter(is_valid, real_passports))
print(valid_count)

def validate_year(year, miny, maxy):
	try:
		iyear = int(year)
		return iyear >= miny and iyear <= maxy
	except:
		return False

def validate_byr(year):
	return validate_year(year, 1920, 2002)

def validate_iyr(year):
	return validate_year(year, 2010, 2020)

def validate_eyr(year):
	return validate_year(year, 2020, 2030)

import re
def validate_hgt(hgt):
	m = re.match(r'(\d*?)(cm|in)', hgt)
	if not m:
		return False
	val, units = m.groups()
	val = int(val)
	if units == 'cm':
		return val >= 150 and val <= 193
	else:
		return val >= 59 and val <= 76

def validate_hcl(hcl):
	return bool(re.match('#[0-9a-f]{6}', hcl))

def validate_ecl(ecl):
	return ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def validate_pid(pid):
	return pid.isdigit() and len(pid) == 9


def is_valid_2(passport):
	if not is_valid(passport):
		return False
	return all([
		validate_byr(passport['byr']),
		validate_iyr(passport['iyr']),
		validate_eyr(passport['eyr']),
		validate_hgt(passport['hgt']),
		validate_hcl(passport['hcl']),
		validate_ecl(passport['ecl']),
		validate_pid(passport['pid']),
	])

test_passports_2_invalid = parse_passports('4.2-invalid.txt')
test_passports_2_valid = parse_passports('4.2-valid.txt')

assert not any(map(is_valid_2, test_passports_2_invalid))
assert all(map(is_valid_2, test_passports_2_valid))

print(len(list(filter(is_valid_2, real_passports))))