from ..utils import iterlines

class Operation:
    def cycle(self, state):
        return state
    
    def end_cycle(self, state):
        return state, True

class Noop(Operation):
    ...

class Add(Operation):
    def __init__(self, n):
        self.n = n
        self.waited_a_tick = False
    
    def end_cycle(self, state):
        done = False
        if self.waited_a_tick:
            state[0] += self.n
            done = True
        else:
            self.waited_a_tick = True
        return state, done

def iter_instructions(test_case=None):
    for line in iterlines(10, test_case=test_case):
        tokens = line.split()
        if tokens[0] == 'noop':
            yield Noop()
        elif tokens[0] == 'addx':
            yield Add(int(tokens[1]))
        else:
            raise Exception

class Sampler:
    def __init__(self, predicate):
        self.predicate = predicate

    def sample(self, i, state):
        if self.predicate(i):
            self._sample(i, state)
            
class PrintSampler(Sampler):
    def _sample(self, _, state):
        print(state)
        
class AccumulatorSampler(Sampler):
    def __init__(self, predicate):
        super().__init__(predicate)
        self.values = []
    
    def _sample(self, i, state):
        self.values.append((i, state[0]))
    
    def sum_signal_strengths(self):
        return sum([val * clock for clock, val in self.values])

class TVPrinterSampler(Sampler):
    def __init__(self):
        super().__init__(every_tick)
        self.row_len = 40
        self.current_row = []
        
    def _sample(self, i, state):
        cursor_location = (i-1) % self.row_len
        if cursor_location in (state[0] - 1, state[0], state[0] + 1):
            self.current_row.append("#")
        else:
            self.current_row.append(".")
        if len(self.current_row) == self.row_len:
            print("".join(self.current_row))
            self.current_row = []

def compute(sampler, test_case=None, debug=False):
    state = [1]
    instr = iter_instructions(test_case)
    current_instruction = next(instr)
    i = 0
    print("Starting computation")
    while True:
        i += 1
        state = current_instruction.cycle(state)
        sampler.sample(i, state)
        state, instruction_complete = current_instruction.end_cycle(state)
        if instruction_complete:
            try:
                current_instruction = next(instr)
            except StopIteration:
                print(f"Instructions ended after cycle {i}")
                return


def every_tick(i):
    return True

def tick_20_then_40(i):
    if i < 20:
        return False
    elif i == 20:
        return True
    else:
        return (i - 20) % 40 == 0
            
# compute(print_every_tick, 1)
compute(PrintSampler(tick_20_then_40), 2)
sampler = AccumulatorSampler(tick_20_then_40)
compute(sampler, 2)
print(sampler.sum_signal_strengths())

sampler = AccumulatorSampler(tick_20_then_40)
compute(sampler)
print(sampler.sum_signal_strengths())

compute(TVPrinterSampler())
