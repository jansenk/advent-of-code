"""
This one was great :) I could have probably done the 16 functions better, but whatevs!
I abslutely misunderstood part one, I thought we were supposed to fugure out which NUMBERS, after
running all tests, had three or more possible outcomes.

Then I was stuck at part two for a while, before I realized you could just do a filter thing.

Rewarding question, five stars
"""


def output(registers, c, val):
    result = registers[:]
    result[c] = val
    return result


def addx(r, a, b, c):
    return output(r, c, a + b)

def addr(r, a, b, c):
    return addx(r, r[a], r[b], c)

def addi(r, a, b, c):
    return addx(r, r[a], b, c)

def mulx(r, a, b, c):
    return output(r, c, a*b)

def mulr(r, a, b, c):
    return mulx(r, r[a], r[b], c)

def muli(r, a, b, c):
    return mulx(r, r[a], b, c)

def banx(r, a, b, c):
    return output(r, c, a & b)

def banr(r, a, b, c):
    return banx(r, r[a], r[b], c)

def bani(r, a, b, c):
    return banx(r, r[a], b, c)

def borx(r, a, b, c):
    return output(r, c, a | b)

def borr(r, a, b, c):
    return borx(r, r[a], r[b], c)

def bori(r, a, b, c):
    return borx(r, r[a], b, c)

def setx(r, a, c):
    return output(r, c, a)

def setr(r, a, b, c):
    return setx(r, r[a], c)

def seti(r, a, b, c):
    return setx(r, a, c)

def gtx(r, a, b, c):
    return output(r, c, 1 if a > b else 0)

def gtir(r, a, b, c):
    return gtx(r, a, r[b], c)

def gtri(r, a, b, c):
    return gtx(r, r[a], b, c)

def gtrr(r, a, b, c):
    return gtx(r, r[a], r[b], c)

def eqx(r, a, b, c):
    return output(r, c, 1 if a == b else 0)

def eqir(r, a, b, c):
    return eqx(r, a, r[b], c)

def eqri(r, a, b, c):
    return eqx(r, r[a], b, c)

def eqrr(r, a, b, c):
    return eqx(r, r[a], r[b], c)

fs = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "banr": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr,
}

import re
t = re.compile("(Before|After): *\[(\d), (\d), (\d), (\d)\]")
def readNextThree(file):
    # Before: [1, 2, 0, 1]
    # 6022
    # After: [1, 2, 0, 1]
    result = []
    l = file.readline()
    #print(1, l)
    if not l.strip():
        l = file.readline()
        #print(2, l)
    if l.strip() == "PART 2":
        return False
    g1 = t.match(l).groups()
    #print(g1)
    result.append(map(int, g1[1:]))
    l = file.readline()
    #print(3, l)
    result.append(map(int, l.strip().split(" ")))
    l = file.readline()
    #print(4, l)
    g2 = t.match(l).groups()
    #print(g2)
    result.append(map(int, g2[1:]))
    file.readline()
    return result

f = open("16in")

x = dict()

from collections import defaultdict
res = defaultdict(lambda: [])
p1r = 0
while True:
    i = readNextThree(f)
    if not i:
        break
    prev = i[0]
    command = i[1]
    after = i[2]
    matches = set()
    for fnct_name in fs:
        fnct_r = fs[fnct_name](prev, command[1], command[2], command[3])
        if fnct_r == after:
            matches.add(fnct_name)
    if len(matches) >= 3:
        p1r += 1
    res[command[0]].append(matches)


smushed = {c: set.intersection(*m) for c, m in res.items()}
print(smushed)

actual_values = {c: None for c in smushed}
print(actual_values)
done_count = 0
while smushed:
    done_c, done_f = (None, None)
    for code, potentials in smushed.items():
        if len(potentials) == 1:
            done_c = code
            done_f = next(iter(potentials))
    if done_c is None:
        raise Exception("Nothing's for sure!!!!")
    done_count += 1
    print("For sure: %d is %s" % (done_c, done_f))
    actual_values[done_c] = done_f
    smushed.pop(done_c, None)
    for c in smushed:
        if done_f in smushed[c]:
            smushed[c].remove(done_f)

print(actual_values)


registers = [0, 0, 0, 0]
for line in f:
    cmd = map(int, line.split(" "))
    funct = actual_values[cmd[0]]
    registers = fs[funct](registers, cmd[1], cmd[2], cmd[3])

print(registers)
