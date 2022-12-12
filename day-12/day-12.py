import os

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

# it's just BFS
def shortest_path(start, end, topography):
    width, height = len(topography), len(topography[0])
    distances = [[-1] * len(row) for row in topography]
    distances[start[0]][start[1]] = 0
    q = [start]
    while len(q) > 0:
        v = q.pop(0)
        if v == end:
            return distances[v[0]][v[1]]
        for i in range(4):
            w = (v[0] + ROW_DIFF[i], v[1] + COL_DIFF[i]) 
            if 0 <= w[0] and w[0] < width and 0 <= w[1] and w[1] < height and \
                    distances[w[0]][w[1]] == -1 and \
                    can_go(topography[v[0]][v[1]], topography[w[0]][w[1]]):
                distances[w[0]][w[1]] = distances[v[0]][v[1]] + 1
                q.append(w)
    return width * height

def part1(lines):
    start, end, topography = parse(lines)
    return shortest_path(start, end, topography)

# initially I calculated the distance to end from each 'a' but this is way faster
# take care, we swapped to and from here since we're going backwards
def shortest_from_end(end, topography):
    width, height = len(topography), len(topography[0])
    distances = [[-1] * len(row) for row in topography]
    distances[end[0]][end[1]] = 0
    q = [end]
    shortest = width * height
    while len(q) > 0:
        v = q.pop(0)
        if topography[v[0]][v[1]] == 0 and distances[v[0]][v[1]] < shortest:
            shortest = distances[v[0]][v[1]]
        for i in range(4):
            w = (v[0] + ROW_DIFF[i], v[1] + COL_DIFF[i]) 
            if 0 <= w[0] and w[0] < width and 0 <= w[1] and w[1] < height and \
                    distances[w[0]][w[1]] == -1 and \
                    can_go(topography[w[0]][w[1]], topography[v[0]][v[1]]):
                distances[w[0]][w[1]] = distances[v[0]][v[1]] + 1
                q.append(w)
    return shortest

def part2(lines):
    _, end, topography = parse(lines)
    return shortest_from_end(end, topography)

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-12.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Shortest path for part 1:", part1(lines))
    print("Shortest path for part 2:", part2(lines))

if __name__ == "__main__":
    main()