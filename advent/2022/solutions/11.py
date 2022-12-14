from math import prod
from ..utils import iter_chunks, iterlines

DIVIDE_BY_THREE = 'div3'
MOD_COMMON_PROD = 'modprod'

def read_chunk(lines):
    try:
        chunk = [next(lines) for _ in range(6)]
    except StopIteration:
        return None
    try:
        next(lines)
    except StopIteration:
        pass
    return chunk

def parse_monkeys(is_test):
    monkeys = []
    lines = iterlines(11, is_test=is_test)
    while (chunk := read_chunk(lines)):        
        monkeys.append(parse_monkey(chunk))
    return monkeys    

class Monkey:
    def __init__(
        self,
        starting_items,
        operation,
        opval,
        test_divisible,
        true_throw,
        false_throw
    ):
        self.items = starting_items
        self.operation = operation
        try:
            self.opval = int(opval)
        except ValueError:
            self.opval = opval
        self.test_divisibility = test_divisible
        self.true_throw = true_throw
        self.false_throw = false_throw
        self.items_inspected = 0
    
    def do_round(self, monkeys, divide_func):
        for item in self.items:
            new_item_val = self.inspect(item, divide_func)            
            if new_item_val % self.test_divisibility == 0:
                monkeys[self.true_throw].items.append(new_item_val)
            else:
                monkeys[self.false_throw].items.append(new_item_val)
        self.items_inspected += len(self.items)
        self.items = []
    
    def inspect(self, item, divide_func):
        if self.opval == "old":
            op_val = lambda x: x
        else:
            op_val = lambda x: self.opval
    
        if self.operation == '+':
            op = lambda y: y + op_val(y)
        elif self.operation == '*':
            op = lambda y: y * op_val(y)
        else:
            raise Exception
        
        new_val = op(item)
        new_val = divide_func(new_val)
        return new_val

import re

pattern = r"""Monkey (?P<id>\d):
Starting items: (?P<starting_items>(((\d+)(, )?)+))
Operation: new = old (?P<operator>.) (?P<opval>((\d+)|old))
Test: divisible by (?P<divisible_test>(\d+))
If true: throw to monkey (?P<true_throw>\d)
If false: throw to monkey (?P<false_throw>\d)"""

def parse_monkey(monkey_chunk):
    monkey_str = "\n".join(monkey_chunk)
    m = re.match(pattern, monkey_str)
    if m is None:
        breakpoint()
    return Monkey(
        list(map(int, m['starting_items'].split(', '))),
        m['operator'],
        m['opval'],
        int(m['divisible_test']),
        int(m['true_throw']),
        int(m['false_throw']),
    )
    
def print_monkeys(round, monkeys):
    print(f"Round {round}")
    # for i, monkey in enumerate(monkeys):
    #     m_s = ", ".join(list(map(str, monkey.items)))
    #     print(f"Monkey {i}: {m_s}")
    for i, monkey in enumerate(monkeys):
        print(f"Monkey {i} inspected {monkey.items_inspected} items")

def throw_around(is_test, divide_mode, reps):
    monkeys = parse_monkeys(is_test)
    mod_prod = prod([monkey.test_divisibility for monkey in monkeys])
    if divide_mode == DIVIDE_BY_THREE:
        divide_func = lambda y: int(y/3)
    else:
        divide_func = lambda y: y % mod_prod
    print_rounds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20]
    print_monkeys(0, monkeys)
    for round in range(1, reps + 1):
        for monkey in monkeys:
            monkey.do_round(monkeys, divide_func)
        if round in print_rounds or (round % 1000 == 0):
            print_monkeys(round, monkeys)
    items = [monkey.items_inspected for monkey in monkeys]
    items.sort()
    print(items[-1] * items[-2])

def part1(is_test):
    throw_around(is_test, DIVIDE_BY_THREE, 20)
    
def part2(is_test):
    throw_around(is_test, MOD_COMMON_PROD, 10_000)

part2(False)