class WrapAroundIterator:
	def __init__(self, a, step=1):
		self.a = a
		self.i = 0
		self.step = step

	def __iter__(self):
		return self

	def __next__(self):
		l = len(self.a)
		if self.i >= l:
			raise StopIteration
		
		value = self.a[self.i]
		next_index = self.i +1
		if next_index == l:
			next_value = self.a[0]
		else:
			next_value = self.a[next_index]
		
		self.i = next_index
		
		return value, next_value
		
class WrapAroundList:
	def __init__(self, l):
		self.l = l

	def __len__(self):
		return len(self.l)
	
	def __iter__(self):
		return iter(self.l)

	def adjust_index(self, a):
		l = len(self)
		if a >= l:
			a = a%l
		return a

	def __getitem__(self, a):
		adjusted = self.adjust_index(a)
		return self.l[adjusted]

	def __setitem__(self, a, val):
		adjusted = self.adjust_index(a)
		self.l[adjusted] = val