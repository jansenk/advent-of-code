"""
Wow, this was a hell of a problem.
Part one seemed too easy, should have been a dead giveaway that part 2 would be a killer.

I needed to find the pattern in what was happening, which was a pain in the ass, and then realize what the two counters
at registers 0 and 1 actually were counting (the sum of the factors of whatever <target> below is)

I can only hope the remaining problems are this hard.
"""

def output(registers, c, val):
    registers[c] = val

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

import time
example = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""

def parse_line(line):
    s = line.split()
    return [sv if si == 0 else int(sv) for si, sv in enumerate(s)]

def call(line, r):
    fs[line[0]](r, line[1], line[2], line[3])

registers = [0, 0, 0, 0, 0, 0]

program = [parse_line(line) for line in open("19in")]
ip = program.pop(0)[1]
print(program)

# while registers[ip] < len(program):
#     line = program[registers[ip]]
#     call(line, registers)
#     registers[ip] += 1
#
# print(registers[0])
#registers = [7, 4, 10551376, 0, 8, 10551376]
#registers = [3, 4, 10551376, 10551376, 4, 2637844]
#registers = [3, 3, 10551376, 31654128, 4, 10551376]
#registers = [3, 2, 10551376, 0, 9, 10551376]
#registers = [1, 2, 10551376, 10551374, 4, 5275687]
#registers = [0, 1, 10551376, 10551376, 4, 10551376]
#registers = [1, 0, 0, 0, 0, 0]
# while registers[ip] < len(program):
#     line = program[registers[ip]]
#     print(line)
#     call(line, registers)
#     registers[ip] += 1
#     print(registers)
#     time.sleep(.75)

final_sum = 0
target = 10551376
for i in range(1, target+1):
    if target % i == 0:
        final_sum += i
        print(i)

print(final_sum)


