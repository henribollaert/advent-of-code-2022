import os

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

ROW_DIFF = [ -1 , 0 , +1 , 0]
COL_DIF = [0, +1, 0, -1]

class Tree:
    def __init__(self, height) -> None:
        self.height = height
        self.max_level = [-1 for _ in range(4)]

    def get_string(self):
        return str(self.height)

def update_in_place(trees, row, col, direction):
    trees[row][col].max_level[direction] = \
        max(trees[row][col].max_level[direction],
            trees[row + ROW_DIFF[direction]][col + COL_DIF[direction]].max_level[direction], 
            trees[row + ROW_DIFF[direction]][col + COL_DIF[direction]].height)
    return trees

def fill_levels(trees):
    # keeping track of the highest tree in each direction
    # first we check west and north
    for row in range(1, len(trees) - 1):
        for col in range(1, len(trees[row]) - 1):
            for direction in [NORTH, WEST]:
                update_in_place(trees, row, col, direction)
    # then we check east and south
    for row in reversed(range(1, len(trees) - 1)):
        for col in reversed(range(1, len(trees[row]) - 1)):
            for direction in [SOUTH, EAST]:
                update_in_place(trees, row, col, direction)
    return trees


def parse(lines):
    rows = []
    for line in lines:
        rows.append([Tree(int(i)) for i in line.strip()])
    return rows

def count_visible_trees(trees):
    return sum([any([tree.height > limit for limit in tree.max_level]) for row in trees for tree in row])

def part1(lines):
    trees = parse(lines)
    trees = fill_levels(trees)
    return count_visible_trees(trees)


def explicit_looking(trees):
    max_scenic_score = -1
    # outside trees have score 0
    for row in range(1, len(trees) - 1):
        for col in range(1, len(trees[row]) - 1):
            scenic_score = 1
            for direction in DIRECTIONS:
                # look in the right direction untill we encounter a tree of at least the same height or the edge
                look_row, look_col = row + ROW_DIFF[direction], col + COL_DIF[direction]
                looking_distance = 1
                while(0 <= look_row and look_row < len(trees) and
                      0 <= look_col and look_col < len(trees[row]) and
                      trees[look_row][look_col].height < trees[row][col].height):
                    look_row += ROW_DIFF[direction]
                    look_col += COL_DIF[direction]
                    looking_distance += 1
                # if we reached the edge, we have counted one tree too many (the edge is not a tree)
                looking_distance -= (look_row < 0 or look_row == len(trees) or look_col < 0 or look_col == len(trees[row]))
                scenic_score *= looking_distance
            max_scenic_score = max(scenic_score, max_scenic_score)
    return max_scenic_score


def part2(lines):
    trees = parse(lines)
    return explicit_looking(trees)

test = ["30373", "25512", "65332", "33549", "35390"]

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-8.txt'), 'r')
    lines = f.readlines()
    f.close()

    # lines = test

    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))

if __name__ == "__main__":
    main()