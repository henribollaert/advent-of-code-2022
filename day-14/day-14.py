import os
from timeit import default_timer as timer

SAND_ORIGIN = (500, 0) # (width, height)

class Simulator:
    def __init__(self, origin, stone_array) -> None:
        self.origin = origin
        self.stone_array = stone_array
        self.depth = len(stone_array)
        self.width = len(stone_array[0])

    def print_stones(self):
        for line in self.stone_array:
            print(line)
        print()

    def drop_sand(self):
        x, y = self.origin
        moved = True
        while(moved):
            if y + 1 < self.depth:
                if self.stone_array[y + 1][x] == '.':
                    y += 1
                else:
                    if x - 1 < 0:
                        return False
                    else:
                        if self.stone_array[y+1][x - 1] == '.':
                            y += 1
                            x -= 1
                        elif x + 1 > self.width:
                            return False
                        elif self.stone_array[y+1][x+1] == '.':
                            y += 1
                            x += 1
                        else:
                            moved = False
            else:
                return False
        if 0 <= x < self.width and 0 <= y < self.depth:
            self.stone_array[y][x] = 'o'
            return True
        return False

    def simulate(self):
        amount = 0
        while(self.drop_sand()):
            amount += 1
        return amount


def parse(lines):
    max_left = max_right = 500
    max_depth = 0
    stones = set()
    for line in lines:
        points = line.split('->')
        prev_x, prev_y = points[0].strip().split(',')
        prev_x, prev_y = int(prev_x), int(prev_y)
        i = 1
        while i < len(points):
            max_left = min(prev_x, max_left)
            max_right = max(prev_x, max_right)
            max_depth = max(prev_y, max_depth)
            cur_x, cur_y = points[i].strip().split(',')
            cur_x, cur_y = int(cur_x), int(cur_y)
            if cur_x == prev_x:
                for y in range(min(cur_y, prev_y), max(cur_y, prev_y) + 1):
                    stones.add((cur_x, y))
            else:
                for x in range(min(cur_x, prev_x), max(cur_x, prev_x) + 1):
                    stones.add((x, cur_y))
            prev_x, prev_y = cur_x, cur_y
            i += 1
        max_left = min(prev_x, max_left)
        max_right = max(prev_x, max_right)
        max_depth = max(prev_y, max_depth)
    # x is second argument to the list (the column), y is the first (the row)
    stone_array = [['.' for _ in range(max_left, max_right+1)] for _ in range(max_depth + 1)]
    x_offset = max_left
    origin = (SAND_ORIGIN[0] - x_offset, SAND_ORIGIN[1])
    stone_array[origin[1]][origin[0]] = '+'
    for x,y in stones:
        stone_array[y][x - x_offset] = '#'
    return origin, stone_array

def part1(lines):
    origin, stone_array = parse(lines)
    sim = Simulator(origin, stone_array)
    return sim.simulate()


'''
What's the idea? The only unfilled spots are the walls and triangles below the walls.
To avoid having to keep track of the triangles and their intersections with other
triangles or walls, I just overwrote the empty spots with
wall symbols and kept the original logic intact. Pretty fast!
'''
def part2(lines):
    start = timer()
    origin, stone_array = parse(lines)
    end = timer()
    print(f'Parsing: {(end-start)*1000}ms')

    start = timer()
    filled_spots = [origin]  # the origin must be filled
    # now we check 
    for row in range(1, len(stone_array)):
        for to_check in range(origin[0] - row, origin[0] + row + 1):
            if not (0 <= to_check < len(stone_array[row]) and
                   (stone_array[row][to_check] == '#' or
                     (to_check > 0 and
                      stone_array[row - 1][to_check - 1] == '#' and
                      stone_array[row - 1][to_check] == '#' and 
                      to_check < len(stone_array[row]) - 1 and
                      stone_array[row - 1][to_check + 1] == '#'))):
                    filled_spots.append((to_check, row))
            else:
                    stone_array[row][to_check] = '#'
            

    # then we check the bottom row
    for to_check in range(origin[0] - len(stone_array), origin[0] + len(stone_array) + 1):
        if not (0 < to_check < len(stone_array[-1]) - 1 and
                stone_array[- 1][to_check - 1] == '#' and
                stone_array[- 1][to_check] == '#' and 
                stone_array[- 1][to_check + 1] == '#'):
            filled_spots.append((to_check, len(stone_array)))
            
    
    end = timer()
    print(f'Actual logic: {(end-start)*1000}ms')

    return len(filled_spots)

    


def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-14.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines))
    start = timer()
    score = part2(lines)
    end = timer()
    print(f"Score for part 2 is {score} in {(end - start)*1000}ms")
    

if __name__ == "__main__":
    main()