import os

# we start counting 0,0 from bottom left corner and increase x to right and y to up

X_DIF = {'R' : 1, 'U' : 0,  'D' : 0, 'L' : -1}
Y_DIF = {'R' : 0, 'U' : 1,  'D' : -1, 'L' : 0}

def distance(pair1, pair2):
    """calculate chebyshev distance"""
    return max(abs(pair1[0] - pair2[0]), abs(pair1[1] - pair2[1]))

def manhattan_length(pair):
    return sum([abs(c) for c in pair])

def part1(lines, verbose=False):
    head = (0,0)
    tail = (0,0)
    tail_positions = set([tail])
    for line in lines:
        direction, amount = line.split()            
        for _ in range(int(amount)):
            prev = head
            head = tuple(map(sum, zip(head, (X_DIF[direction], Y_DIF[direction]))))
            if distance(head, tail) > 1:
                tail = prev
                tail_positions.add(tail)
        if verbose:
            print(f"===== {direction} {amount} =====\nhead: {head}\ntail: {tail}")
    return len(tail_positions)

def simulate_rope(moves, length):
    """
    length = numbered knots so H, 1, 2, ..., 9 has length 9
    """
    head = (0,0)
    knots = [(0,0) for _ in range(length)]
    tail_positions = set([knots[-1]])
    tail_list = [knots[-1]]
    for direction, amount in moves:
        for _ in range (amount):
            prev = head
            head = tuple(map(sum, zip(head, (X_DIF[direction], Y_DIF[direction]))))
            # first
            cur = knots[0]
            if distance(head, knots[0]) > 1:
                knots[0] = prev
            prev_move_length = manhattan_length((knots[0][0] - cur[0], knots[0][1] - cur[1]))
            prev = cur

            # rest
            i = 1
            while i < length and distance(knots[i - 1], knots[i]) > 1:
                cur = knots[i]
                if prev_move_length == 1:
                    # classic
                    knots[i] = prev
                else:
                    # longer
                    new_x, new_y = knots[i]
                    if knots[i-1][0] < knots[i][0]:
                        new_x -= 1
                    elif knots[i-1][0] > knots[i][0]:
                        new_x += 1

                    if knots[i-1][1] < knots[i][1]:
                        new_y -= 1
                    elif knots[i-1][1] > knots[i][1]:
                        new_y += 1
                    knots[i] = (new_x, new_y)
                    # knots[i] = tuple(map(sum, zip(knots[i], prev_move)))
                # if knots[i - 1][0] != knots[i][0] and knots[i - 1][1] != knots[i][1]:
                #     # is this wrong?
                #     if sum([abs(c) for c in prev_move]) > 1:
                #         knots[i] = tuple(map(sum, zip(knots[i], prev_move)))
                #     else:
                #         knots[i] = prev
                # else:
                #     knots[i] = tuple(map(sum, zip(knots[i], (X_DIF[direction], Y_DIF[direction]))))
                prev_move_length = manhattan_length((knots[i][0] - cur[0], knots[i][1] - cur[1]))
                prev = cur
                i += 1
            tail_positions.add(knots[-1])
            tail_list.append(knots[-1])
    return len(tail_positions)

def part2(lines):
    moves = [(line.split()[0], int(line.split()[1])) for line in lines]
    return simulate_rope(moves, length=9)

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-9.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))


if __name__ == "__main__":
    main()