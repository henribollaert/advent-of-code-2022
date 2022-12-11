import os
from math import prod
import operator

class Monkey():

    def __init__(self, nr, starting_items, operation, test, relief) -> None:
        self.nr = nr
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.inspections = 0
        self.relief = relief

    def take_turn(self, monkeys, verbose=False):
        if verbose:
            print(f" Monkey {self.nr}")
        for item in self.items:
            # inspect
            new_item = self.operation(item)
            # check worry level
            new_item = self.relief(new_item)
            if verbose:
                print(f"{item} becomes {new_item}")
            self.inspections += 1
            # test and throw
            if verbose:
                print(f"target: {self.test(new_item)}")
            monkeys[self.test(new_item)].items.append(new_item)
        self.items = []


    def print_monkey(self):
        print(f'Monkey {self.nr}:')
        print(f'  Items: {self.items}')
        print(f'  Operation on 1: {self.operation(1)}')
        print(f'  Test on 1: {self.test(1)}')

    def print_items(self):
        print(f'Monkey {self.nr}: {self.items}')

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
                test = lambda x, true_monkey=true_monkey, divisor=divisor, false_monkey=false_monkey: true_monkey if x % divisor == 0 else false_monkey
                monkey_values.append([starting_items, operation, test])
        i += 1
    
    return monkey_values, divisors

def create_monkeys(monkey_values, relief= None, divisors = None):
    if relief == None:
        assert divisors != None
        limit = prod(divisors)
        relief = lambda x : x % limit
    monkeys = []
    for nr, values in enumerate(monkey_values):
        monkeys.append(Monkey(nr, *values, relief=relief))
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

def watch_monkeys(monkeys, rounds, verbose = False):
    for i in range(rounds):
        for monkey in monkeys:
            monkey.take_turn(monkeys)
        if verbose:
            print(f"===== Round {i + 1} =====")
            for monkey in monkeys:
                monkey.print_items()
    return calculate_monkey_business(monkeys)

def part1(lines):
    monkey_values, _ = parse(lines)
    monkeys = create_monkeys(monkey_values, relief = lambda x : x // 3)
    return watch_monkeys(monkeys, rounds=20)

def part2(lines):
    monkey_values, divisors = parse(lines)
    monkeys = create_monkeys(monkey_values, divisors=divisors)
    return watch_monkeys(monkeys, rounds=10000)
    

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-11.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))


if __name__ == "__main__":
    main()
