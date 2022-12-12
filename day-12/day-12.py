import os
from collections import deque

OFFSET = ord('a')

def parse(input):
    topography = []
    start, end = None, None
    for row, line in enumerate(input):
        r = []
        for column, letter in enumerate(line.strip()):
            height =  ord(letter) - OFFSET
            if letter == 'S':
                start = (row, column)
                height = 0
            elif letter == 'E':
                end = (row, column)
                height = 25
            
            r.append(height)
        topography.append(r)

    return start, end, topography

def can_go(f, t):
    return t <= f + 1

ROW_DIFF = [ -1 , 0 , +1 , 0]
COL_DIFF = [0, +1, 0, -1]

# it's just BFS, but we go in reverse, because that makes part 2 easier
def shortest_path(start, end, topography):
    width, height = len(topography), len(topography[0])
    distances = [[-1] * len(row) for row in topography]
    distances[end[0]][end[1]] = 0
    q = deque([end])
    while len(q) > 0:
        v_x, v_y = q.popleft()
        if (v_x, v_y) == start or (start == None and topography[v_x][v_y] == 0):
            return distances[v_x][v_y]
        for i in range(4):
            w_x, w_y = v_x + ROW_DIFF[i], v_y + COL_DIFF[i]
            if 0 <= w_x < width and 0 <= w_y < height and distances[w_x][w_y] == -1 and \
                    can_go(topography[w_x][w_y], topography[v_x][v_y]):
                distances[w_x][w_y] = distances[v_x][v_y] + 1
                q.append((w_x, w_y))

def part1(lines):
    start, end, topography = parse(lines)
    return shortest_path(start, end, topography)

# initially I calculated the distance to end from each 'a' but this way is faster
# take care, we swapped to and from here since we're going backwards
def part2(lines):
    _, end, topography = parse(lines)
    return shortest_path(None, end, topography)

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-12.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Shortest path for part 1:", part1(lines))
    print("Shortest path for part 2:", part2(lines))

if __name__ == "__main__":
    main()