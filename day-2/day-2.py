import os



def part1(lines):
    playing_scores = {'X' : 1, 'Y' : 2, 'Z' : 3}
    score_A = {'X' : 3, 'Y' : 6, 'Z' : 0}
    score_B = {'X' : 0, 'Y' : 3, 'Z' : 6}
    score_C = {'X' : 6, 'Y' : 0, 'Z' : 3}
    score_table = {'A' : score_A, 'B' : score_B, 'C' : score_C}

    total_score = 0

    for line in lines:
        hands  = line.split()
        total_score += playing_scores[hands[1]] + score_table[hands[0]][hands[1]]

    return total_score

def part2(lines):
    result_scores = {'X' : 0, 'Y' : 3, 'Z' : 6}
    score_A = {'X' : 3, 'Y' : 1, 'Z' : 2}
    score_B = {'X' : 1, 'Y' : 2, 'Z' : 3}
    score_C = {'X' : 2, 'Y' : 3, 'Z' : 1}
    score_table = {'A' : score_A, 'B' : score_B, 'C' : score_C}

    total_score = 0

    for line in lines:
        hands = line.split()
        total_score += result_scores[hands[1]] + score_table[hands[0]][hands[1]]

    return total_score



def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-2.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))

if __name__ == "__main__":
    main()
