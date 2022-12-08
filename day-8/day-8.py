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

def part1(lines):
    trees = parse(lines)
    trees = fill_levels(trees)
    # now we count the visible trees
    nr_visible_trees = 0
    for row in trees:
        for tree in row:
            if any([tree.height > limit for limit in tree.max_level]):
                nr_visible_trees += 1
    return nr_visible_trees


def explicit_looking(trees):
    max_scenic_score = -1
    for row in range(1, len(trees) - 1):
        for col in range(1, len(trees[row]) - 1):
            scenic_score = 1
            for direction in DIRECTIONS:
                temp_i = row + ROW_DIFF[direction]
                temp_j = col + COL_DIF[direction]
                length = 1
                while(0 <= temp_i and temp_i < len(trees) and
                      0 <= temp_j and temp_j < len(trees[row]) and
                      trees[temp_i][temp_j].height < trees[row][col].height):
                    temp_i += ROW_DIFF[direction]
                    temp_j += COL_DIF[direction]
                    length += 1
                if(temp_i < 0 or temp_i == len(trees) or temp_j < 0 or temp_j == len(trees[row])):
                    length -= 1
                scenic_score *= length
            if  scenic_score > max_scenic_score:
                max_scenic_score = scenic_score
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