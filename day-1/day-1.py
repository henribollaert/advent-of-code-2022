import os


def get_top(lines, nr):
    max_sums = [0 for _ in range(nr)]
    cur_sum = 0
    for line in lines:
        if line == '\n':
            i = 0
            while (i < nr and cur_sum < max_sums[i]):
                i += 1
            if(i < nr):
                j = len(max_sums) - 1
                while(j > i):
                    max_sums[j] = max_sums[j-1]
                    j -= 1
                max_sums[i] = cur_sum
            cur_sum = 0
        else:
            cur_sum += int(line)
    return sum(max_sums)

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-1.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("The answer to part 1 is", get_top(lines, 1))
    print("The answer to part 2 is", get_top(lines, 3))

if __name__ == "__main__":
    main()
