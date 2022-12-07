import os

def part1_old(line, marker_length = 4):
    marker = list(line[:marker_length - 1])
    i = marker_length - 1
    while (i < len(line) and line[i] in marker):
        move = marker.index(line[i])
        marker[i % (marker_length - 1)] = line[i]
        i += 1
        print(move)
        for _ in range(move):
            marker[i % (marker_length - 1)] = line[i]
            i += 1
        print("".join(marker))
    print("".join(marker) + line[i])
    return i

def part1(line, marker_length=4):
    i = marker_length
    while(i < len(line) and len(set(line[i - marker_length:i])) != marker_length):
        i += 1
    print(line[i-marker_length:i])
    return i

def part2(line):
    return part1(line, marker_length=14)

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-6.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines[0]))
    print("Score for part 2:", part2(lines[0]))

if __name__ == "__main__":
    main()