import os

def convert_crates(crates):
    nr_of_stacks = int(crates[-1].split()[-1])
    stacks = [[] for _ in range(nr_of_stacks)]
    for i in reversed(range(0, len(crates) - 1)):
        for j in range(nr_of_stacks):
            if crates[i][1 + 4*j] != ' ':
                stacks[j].append(crates[i][1 + 4*j])
    return stacks

def convert_moves(moves):
    new_moves = []
    for move in moves:
        new_move = {}
        info = move.split()
        new_move['amount'] = int(info[1])
        new_move['from'] = int(info[3]) - 1
        new_move['to'] = int(info[5]) - 1
        new_moves.append(new_move)
    return new_moves

def get_crates_and_moves(lines):
    # seperate crates and moves
    crates = []
    i = 0
    while lines[i] != '\n':
        crates.append(lines[i])
        i += 1
    i += 1 # empty line
    moves = []
    while i < len(lines):
        moves.append(lines[i])
        i += 1

    # convert the input crates into lists corresponding to each stack
    stacks = convert_crates(crates)
    # convert the input moves into more informative dicts
    moves = convert_moves(moves)

    return stacks, moves

def one_move(stacks, move):
    stacks[move['to']].append(stacks[move['from']].pop())

def get_word(stacks):
    word = ''
    for stack in stacks:
        word += stack[-1]
    return word

def part1(lines):
    stacks, moves = get_crates_and_moves(lines)
    
    for move in moves:
        for _ in range(move['amount']):
            one_move(stacks, move)
    
    return get_word(stacks)

def multi_move(stacks, move):
    temp = stacks[move['from']][-move['amount']:]
    del stacks[move['from']][-move['amount']:]
    stacks[move['to']].extend(temp)
    

def part2(lines):
    stacks, moves = get_crates_and_moves(lines)
    
    for move in moves:
        multi_move(stacks, move)
    
    return get_word(stacks)

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-5.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))

if __name__ == "__main__":
    main()