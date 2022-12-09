import os

def part1(lines):
    amount = 0
    for line in lines:
        intervals = line.split(',')
        amount += (int(intervals[0].split('-')[0]) <= int(intervals[1].split('-')[0]) and
                   int(intervals[0].split('-')[1]) >= int(intervals[1].split('-')[1])) or \
                  (int(intervals[0].split('-')[0]) >= int(intervals[1].split('-')[0]) and
                   int(intervals[0].split('-')[1]) <= int(intervals[1].split('-')[1]))
    return amount

def part2(lines):
    amount = 0
    for line in lines:
        intervals = line.split(',')
        amount += not (int(intervals[0].split('-')[1]) < int(intervals[1].split('-')[0]) or
                       int(intervals[0].split('-')[0]) > int(intervals[1].split('-')[1]))
    return amount

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-4.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))

if __name__ == "__main__":
    main()