import os

# default offset
OFFSET = ord('a')

def get_priority(c):
    r = 0
    if c.isupper():
        c = c.lower()
        r += 26
    return r + ord(c) - OFFSET + 1
    
def part1(lines):
    score = 0
    for line in lines:
        line = line.strip()
        i = 0
        j = len(line) // 2
        while(i < len(line) / 2 and j < len(line) and line[i] != line[j]):
            j += 1
            if j == len(line):
                i += 1
                j = len(line)//2
        score += get_priority(line[i])
    return score
        
def part2(lines):
    score = 0
    for i in range(len(lines)//3):
        j = 0
        while(j < len(lines[3*i]) and not (lines[3*i][j] in lines[3*i + 1] and 
                            lines[3*i][j] in lines[3*i + 2])):
            j += 1
        score += get_priority(lines[3*i][j])
    return score
        


def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-3.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))

if __name__ == "__main__":
    main()