import os
from functools import cmp_to_key
from math import prod
from json import loads

def get_pairs(input):
    pairs = []
    for i in range((len(input) + 1)//3):
        p1 = eval(input[3*i])
        p2 = eval(input[3*i+1])
        pairs.append((p1,p2))
    return pairs

def get_all(lines):
    packets = []
    for line in lines:
        if len(line) > 1:
            packets.append(eval(line))
    return packets

def compare(l, r):
    if isinstance(l, int) and isinstance(r, int):
        if l == r:
            return 0
        if l < r:
            return -1
        if l > r:
            return 1
    else:
        if isinstance(l, int):
            l = [l]
        if isinstance(r, int):
            r = [r]
        for i in range(min(len(l), len(r))):
            res = compare(l[i], r[i])
            if res != 0:
                return res
        if len(l) == len(r):
            return 0
        if len(l) < len(r):
            return -1
        if len(l) > len(r):
            return 1
    

def part1(lines):
    pairs = get_pairs(lines)
    indices = []
    for index, pair in enumerate(pairs):
        if compare(pair[0], pair[1]) == -1:
            indices.append(index + 1)  # starts from 1 for some stupid reason
    return sum(indices)

def part2(lines, separators = [[[2]], [[6]]]):
    packets = get_all(lines)
    packets.extend(separators)
    packets = sorted(packets, key = cmp_to_key(compare))
    return prod([packets.index(sep)+1 for sep in separators])

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-13.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))

if __name__ == "__main__":
    main()