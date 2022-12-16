from dataclasses import dataclass

def iterlines(day_num, is_test=False, test_case=None):
    test_suffix = '' if test_case is None else str(test_case)
    is_test = is_test or test_case is not None
    test_filename = f'-test{test_suffix}' if is_test else ''
    with open(f'advent/2022/input_files/{day_num}{test_filename}.txt') as f:
        for line in f:
            yield line.strip()
            
def iter_chunks(day_num, chunk_lines, is_test=False, test_case=None):
    lines = iterlines(day_num, is_test=is_test, test_case=test_case)
    while True:
        yield [next(lines) for _ in range(chunk_lines)]

@dataclass
class Range:
    rmin: int = float('inf')
    rmax: int = float('-inf')
    
    def clone(self):
        return Range(self.rmin, self.rmax)
    
    def extend(self, v):
        if v < self.rmin:
            self.rmin = v
        if v > self.rmax:
            self.rmax = v
    
    def contains(self, other):
        return other.rmin in self and other.rmax in self

    def overlaps(self, other):
        return other.rmin in self or other.rmax in self
    
    def combine(self, other):
        return Range(
            min(self.rmin, other.rmin),
            max(self.rmax, other.rmax),
        )
    
    def limit(self, limit):
        limited_min = max(self.rmin, limit.rmin)
        limited_max = min(self.rmax, limit.rmax)
        return Range(limited_min, limited_max)

    def __iter__(self):
        return iter(range(self.rmin, self.rmax + 1))
    
    def __contains__(self, v):
        return self.rmin <= v and v <= self.rmax
    
    def __len__(self):
        return abs(self.rmax - self.rmin) + 1

@dataclass
class Window:
    x_range: Range = Range()
    y_range: Range = Range()
    
    def extend(self, p):
        self.x_range.extend(p.x)
        self.y_range.extend(p.y)
