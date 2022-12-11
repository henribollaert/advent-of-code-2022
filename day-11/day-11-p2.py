"""
Slower version of part 2.
"""
import os
from math import prod
import operator
from functools import reduce

class WorryLevel():

    def __init__(self, initial_value, divisors) -> None:
        self.divisors = divisors
        self.remainders = {d: initial_value % d for d in self.divisors}

    def apply_operation(self, operation):
        self.remainders = {d: operation(self.remainders[d]) % d for d in self.divisors}

class RemainderMonkey():

    def __init__(self, nr, starting_items, operation, test, divisors) -> None:
        self.nr = nr
        self.items = [WorryLevel(item, divisors) for item in starting_items]
        self.operation = operation
        self.test = test
        self.inspections = 0

    def take_turn(self, monkeys, verbose=False):
        if verbose:
            print(f" Monkey {self.nr}")
        for item in self.items:
            # inspect
            item.apply_operation(self.operation)
            self.inspections += 1
            # test and throw
            monkeys[self.test(item)].items.append(item)
        self.items = []

OPS = {'+' : operator.add,
       '-' : operator.sub,
       '*' : operator.mul,
       '/' : operator.floordiv}


def parse(input):  # works
    i = 0
    monkey_values = []
    divisors = [] 
    starting_items = operation = test = None
    while i < len(input):
        words = input[i].split()
        if len(words) != 0:
            if words[0] == 'Starting':
                starting_items = [int(s.strip(',')) for s in words[2:]]
            if words[0] == 'Operation:':
                if words[5] == 'old':
                    operation = lambda x : x*x
                else:
                    operation = lambda x, op = OPS[words[4]], val=int(words[5]): op(x, val)
            if words[0] == 'Test:':
                divisor = int(words[-1])
                divisors.append(divisor)
                i += 1
                true_monkey = int(input[i].split()[-1])
                i+= 1
                false_monkey = int(input[i].split()[-1])
                test = lambda x, true_monkey=true_monkey, divisor=divisor, false_monkey=false_monkey: true_monkey if x.remainders[divisor] == 0 else false_monkey
                monkey_values.append([starting_items, operation, test])
        i += 1
    
    monkeys = []
    for nr, values in enumerate(monkey_values):
        monkeys.append(RemainderMonkey(nr, *values, divisors=divisors))

    return monkeys


def calculate_monkey_business(monkeys, nr=2):
    max_inspections = [0 for _ in range(nr)]
    for monkey in monkeys:
        i = 0
        while (i < nr and monkey.inspections < max_inspections[i]):
            i += 1
        if(i < nr):
            j = len(max_inspections) - 1
            while(j > i):
                max_inspections[j] = max_inspections[j-1]
                j -= 1
            max_inspections[i] = monkey.inspections
    return prod(max_inspections)

    
        
def part2(lines, rounds = 10000):
    monkeys = parse(lines)
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.take_turn(monkeys)
    return calculate_monkey_business(monkeys)

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-11.txt'), 'r')
    lines = f.readlines()
    f.close()

    # print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))

if __name__ == "__main__":
    main()