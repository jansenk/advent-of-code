
def load_instructions(f_n):
	with open('advent2017/input_files/'+f_n) as f:
		instructions = []
		for line in f:
			tokens = line.split()
			if len(tokens) == 3:
				instructions.append(tokens)
			else:
				instructions.append((tokens[0], tokens[1], None))
	return instructions

from collections import defaultdict, deque
class Computer:
	def __init__(self, instructions, p):
		self.instructions = instructions
		self.li = len(instructions)
		self.connection = connection
		self.queue = deque()
		self.waiting_for_input = False
		self.registers = defaultdict(int)
		self.registers['p'] = p
		self.last_freq = None
		self.i = 0
		self.running = True

	def get_value(self, target):
		if isinstance(target, int):
			return target
		try:
			return int(target)
		except:
			return self.registers[target]
	
	def still_waiting_for_value(self):
		return self.waiting_for_input and not self.queue
	
	def	set_value(self, target, value):
		if isinstance(value, int):
			pass # already an int
		try:
			value = int(value)
		except:
			value = self.registers[value]
		self.registers[target] = value

	def run_until_wait(self):
		while self.i >= 0 and self.i < self.li:
			op, x, y = self.instructions[self.i]
			increment = True
			if op == 'snd':
				value = self.get_value(x)
				self.registers['sound'] = value
			elif op == 'set':
				value = self.get_value(y)
				self.set_value(x, value)
			elif op == 'add':
				value = self.get_value(y)
				self.registers[x] += value
			elif op == 'mul':
				value = self.get_value(y)
				self.registers[x] *= value
			elif op == 'mod':
				value = self.get_value(y)
				self.registers[x] %= value
			elif op == 'rcv':
				value = self.get_value(x)
				if value != 0:
					return self.registers['sound']
			elif op == 'jgz':
				x = self.get_value(x)
				y = self.get_value(y)
				if x != 0:
					increment = False
					self.i += y
			elif op == 'snd':
				value = self.get_value(x)
				self.connection.queue.append(value)
			elif op == 'rcv':
				if self.queue:
					value = self.queue.popleft()
					self.registers[x] = value
				else:
					self.waiting_for_input = True
					return
			if increment:
				self.i += 1
		self.running = False

assert Computer(load_instructions('18-test.txt')).run_until_wait() == 4
instructions = load_instructions('18.txt')
print(Computer(load_instructions('18.txt')).run_until_wait())

c0 = Computer(instructions, 0)
c1 = Computer(instructions, 1)
c0.connection = c1
c1.connection = c0

while True:
	c0.run_until_wait()
	c1.run_until_wait()

	
