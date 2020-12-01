class Rule:
	def __init__(self, rule_id):
		self.rule_id = rule_id

	def _load(self, rule_dict):
		for child_rule in self.child_rules:
			self.child_rules[child_rule] = rule_dict[child_rule]

	def matches(self, s):
		match, i = self._matches(s, 0)
		if not match:
			return False
		if i != len(s):
			return False
		return True

	def count_all_times_matched(self, s, i):
		import pdb; pdb.set_trace()
		potential_matches = []
		matches = True
		while matches:
			matches, new_i_s = self._matches(s, i)
			assert len(new_i_s) == 1
			new_i = new_i_s[0]
			if matches:
				potential_matches.append(new_i)
				i = new_i
		return potential_matches

	def __repr__(self):
		return str(self)


class BaseRule(Rule):
	def __init__(self, rule_id, char):
		super().__init__(rule_id)
		self.child_rules = []
		self.char = char
	
	def _matches(self, s, i=0):
		try:
			return s[i] == self.char, i+1
		except IndexError:
			return False, -1
	
	def __str__(self):
		return f'[{self.rule_id}]: "{self.char}"'
	
	def regex(self):
		return self.char

class AndRule(Rule):
	def __init__(self, rule_id, conditions):
		super().__init__(rule_id)
		self.child_rules = {c: None for c in conditions}
		self.conditions = conditions
	
	def _matches(self, s, i=0):
		if i >= len(s):
			return False, -1
		for condition in self.conditions:
			match, i = self.child_rules[condition]._matches(s, i)
			if not match:
				return False, -1
		return True, i
		
	def __str__(self):
		return f'[{self.rule_id}]: "{self.conditions}"'

	def regex(self):
		result = ''
		for condition in self.conditions:
			result += self.child_rules[condition].regex()
		return result

class OrRule(Rule):
	def __init__(self, rule_id, conditional_left, conditional_right, part2_replace=False):
		super().__init__(rule_id)
		self.child_rules = {c: None for c in conditional_left + conditional_right}
		self._cond_left = conditional_left
		self._cond_right = conditional_right
		self.conditional_left = AndRule(-1, conditional_left)
		self.conditional_right = AndRule(-1, conditional_right)
		self.part2_replace = part2_replace
	
	def _load(self, rule_dict):
		super()._load(rule_dict)
		self.conditional_left._load(rule_dict)
		self.conditional_right._load(rule_dict)

	def _matches(self, s, i=0):
		assert not self.part2_replace
		if i >= len(s):
			return False, -1
		left_match = self.conditional_left._matches(s, i)
		if left_match[0]:
			return left_match
		right_match = self.conditional_right._matches(s, i)
		if right_match[0]:
			return right_match
		return False, -1
	
	def __str__(self):
		return f'[{self.rule_id}]: "{self._cond_left}" | "{self._cond_right}"'

	def regex(self):
		leftstr = self.conditional_left.regex()
		rightstr = self.conditional_right.regex()
		return "(" + leftstr + "|" + rightstr + ")" 

class Rule8(Rule):
	def __init__(self):
		self.child_rules = {'42': None}

	def _matches(self, s, i):
		rule42 = self.child_rules['42']
		potential_matches = rule42.count_all_times_matched(s, i)
		if len(potential_matches) > 0:
			return True, potential_matches
		return False, -1
	
	def regex(self):
		return f'({self.child_rules["42"].regex()})+'

class Rule11(Rule):
	def __init__(self):
		self.child_rules = {'42': None, '31': None}
	
	def _matches(self, s, i):
		ultimate_results = []
		rule42 = self.child_rules['42']
		potential_42_matches = rule42.count_all_times_matched(s, i)
		if len(potential_42_matches) == 0:
			return False, -1
		rule31 = self.child_rules['31']
		for number_matches, potential_42_i in enumerate(potential_42_matches, start=1):
			potential_31_matches = rule31.count_all_times_matched(s, potential_42_i)
			if len(potential_31_matches) < number_matches:
				continue
			ultimate_results.append(potential_31_matches[number_matches-1])
		return len(ultimate_results) > 0, ultimate_results
	
	def regex(self):
		return f'({self.child_rules["42"].regex()}){{REPLACE_ME}}({self.child_rules["31"].regex()}){{REPLACE_ME}}'

def read_file(filename, part2_replace=False):
	with open('advent/input_files/'+filename) as f:
		line = f.readline().strip()
		rules = dict()
		while line != '':
			rule_id, rule_text = line.split(': ')
			if part2_replace and rule_id == '8':
				rules[rule_id] = Rule8()
			elif part2_replace and rule_id == '11':
				rules[rule_id] = Rule11()
			elif rule_text in ('"a"', '"b"'):
				char = rule_text[1]
				rules[rule_id] = BaseRule(rule_id, char)
			elif " | " in rule_text:
				tokens = rule_text.split()
				pipe = tokens.index('|')
				rules[rule_id] = OrRule(rule_id, tokens[:pipe], tokens[pipe+1:])
			else:
				rules[rule_id] = AndRule(rule_id, rule_text.split())
			line = f.readline().strip()
		for rule in rules.values():
			rule._load(rules)
		inputs = [line.strip() for line in f]
	return rules, inputs

rules, _= read_file('19.1.txt')
# import pdb; pdb.set_trace()

rule_0 = rules['0']
# assert rule_0.matches('ababbb')
# assert rule_0.matches('abbbab')
# assert not rule_0.matches('bababa')
# assert not rule_0.matches('aaabbb')
# assert not rule_0.matches('aaaabbb')

import re
rule_o_str = rule_0.regex()
assert re.fullmatch(rule_o_str, 'ababbb') is not None
assert re.fullmatch(rule_o_str, 'ababbb') is not None
assert re.fullmatch(rule_o_str, 'bababa') is None
assert re.fullmatch(rule_o_str, 'aaabbb') is None
assert re.fullmatch(rule_o_str, 'aaaabbb') is None

def count_matches_zero(filename, part2_replace):
	rules, inputs = read_file(filename, part2_replace)
	rule_0 = rules['0']
	rule_0_str = rule_0.regex()
	rule_0_pattern = re.compile(rule_0_str)
	result = 0
	for line in inputs:
		if part2_replace:
			for i in range(1, 100):
				rule_str = rule_0_str.replace('REPLACE_ME', str(i))
				match = re.fullmatch(rule_str, line)
				if match is not None:
					break
		else:
			match = rule_0_pattern.fullmatch(line)
		# if rule_0.matches(line):
		if match is not None:
			result += 1
			# assert match is not None
		# else:
			# assert match is None
	print(result)

count_matches_zero('19.1.txt', False)
count_matches_zero('19.txt', False)
count_matches_zero('19.txt', True)

# count_matches_zero('19.2.txt', True)

# rules, inputs = read_file('19.2.txt')
# print(rules['8'].regex().replace('(a|b)', '.'))
# print('---')
# print(rules['11'].regex().replace('(a|b)', '.'))
# rules['0']