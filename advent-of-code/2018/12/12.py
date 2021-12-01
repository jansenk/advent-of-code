"""
Solving this with a couple of sets filled with stringified deques is not how i first thought of this

How I first thought of this was much much worse :L

A combination of lambdas testing each character would be neat ..... also very slow and very stupid

I cheated for part two, before I got the answer I looked at other solutions online, since they weren't code
 I didn't feel so bad. I started running the algo and I thought I was fine because what I had was fast ....
 not fast enough for 50 billion cycles x(
"""

from collections import deque

f = open("in")


def parse_starting_state(starting_str):
    result = set()
    for i in range(len(starting_str)):
        if starting_str[i] == "#":
            result.add(i)
    return result


#This is fun but really not needed, I think I can do this with just a dict
# # really unnecessary and overcomplicated but for some reason i feel drawn to it lol
# def t_to_b(t):
#     return (c == "#" for c in t)
#
def t_to_d(t):
    d = deque(maxlen=5)
    for c in t:
        d.append(c == "#")
    return d
#
# def gen_f(i, s):
#     return lambda x: x[i] == s
#
# def gen_f_set(is_not):
#     if is_not:
#         return lambda i, s: i not in s
#     return lambda i, s: i in s
#
# class PlantFunction:
#     def __init__(self, line):
#         s = line.split(" => ")
#         self.o = s[1]
#         self.t = s[0]
#         self.fss = [gen_f_set(self.t[i] == ".") for i in range(len(self.t))]
#         self.fs = [gen_f(i, self.t[i]) for i in range(len(self.t))]
#
#     def matches(self, seg):
#         return all(map(lambda f: f(seg),self.fs))
#
#     def matches_set(self, s, i):
#         return all(self.fss[c+2](i + c, s) for c in range(-2, 3))
#
#     def __repr__(self):
#         return self.t + " => " + self.o


state = parse_starting_state(f.readline().split(" ")[2])
state_min = min(state)
state_max = max(state)

f.readline()
f_set = set()
for line in f:
    split_line = line.strip().split(" => ")
    bool_key = t_to_d(split_line[0])
    if split_line[1] == "#":
        f_set.add(str(bool_key))

for step in range(1000):
    next_state = set()
    next_min = float('inf')
    next_max = float("-inf")
    current_window = deque(maxlen=5)
    current_window.extend((False, False, False, False, False))
    for i in range(state_min - 2, state_max + 2):
        current_window.append((i + 2) in state)
        if str(current_window) in f_set:
            next_state.add(i)
            if i < next_min:
                next_min = i
            if i > next_max:
                next_max = i
    delta = sum(next_state) - sum(state)
    print("Delta: %d" % delta)
    print(sum(next_state))
    state = next_state
    state_min = next_min
    state_max = next_max

print("estimated step 50 billion")
print(((50000000000 - 1000) * 53) + 53466)












