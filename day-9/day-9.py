import os

# we start counting 0,0 from bottom left corner and increase x to right and y to up

X_DIF = {'R' : 1, 'U' : 0,  'D' : 0, 'L' : -1}
Y_DIF = {'R' : 0, 'U' : 1,  'D' : -1, 'L' : 0}

def sign(a):
    return (a > 0) - (a < 0)

def chebyshev_distance(x1, x2):
    return max([abs(sum(pair)) for pair in zip(x1, [-1 * x for x in x2])])

def manhattan_length(pair):
    return sum([abs(c) for c in pair])

def part1old(lines, verbose=False):
    head = (0,0)
    tail = (0,0)
    tail_positions = set([tail])
    for line in lines:
        direction, amount = line.split()            
        for _ in range(int(amount)):
            prev = head
            head = tuple(map(sum, zip(head, (X_DIF[direction], Y_DIF[direction]))))
            if chebyshev_distance(head, tail) > 1:
                tail = prev
                tail_positions.add(tail)
        if verbose:
            print(f"===== {direction} {amount} =====\nhead: {head}\ntail: {tail}")
    return len(tail_positions)


def simulate_rope(moves, length=10):
    """
    length includes H: H, 1, 2, ..., 9 has length 10
    """
    knots = [(0,0) for _ in range(length)]
    tail_positions = set([knots[-1]])
    for direction, amount in moves:
        for _ in range (amount):
            knots[0] = tuple(map(sum, zip(knots[0], (X_DIF[direction], Y_DIF[direction]))))
            i = 1
            while i < length and chebyshev_distance(knots[i - 1], knots[i]) > 1:
                knots[i] = tuple(map(sum, zip(knots[i], 
                                              (sign(knots[i-1][0] - knots[i][0]),
                                               sign(knots[i-1][1] - knots[i][1])))))
                i += 1
            tail_positions.add(knots[-1])
    return len(tail_positions)

def part1(lines):
    return simulate_rope([(line.split()[0], int(line.split()[1])) for line in lines], 2)

def part2(lines):
    return simulate_rope([(line.split()[0], int(line.split()[1])) for line in lines], 10)

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-9.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))


if __name__ == "__main__":
    main()