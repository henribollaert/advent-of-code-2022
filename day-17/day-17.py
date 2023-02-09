import os
from timeit import default_timer as timer

class Rock:
    def __init__(self, left, min_height) -> None:
        pass

    def move_down(self):
        pass

    def horizontal_move(self, direction):
        pass

    def can_move(self, move):
        if move == 'v':
            return self.move_down()
        elif move == '>':
            self.horizontal_move(1)
        else:
            self.horizontal_move(-1)
        return True

class MinRock(Rock):
    pass

class PlusRock(Rock):
    pass

class LRock(Rock):
    pass

class IRock(Rock):
    pass

class SquareRock(Rock):
    pass
        

class Simulator:
    def __init__(self, jets, rocks=None, width=7) -> None:
        self.jets = jets
        self.jet_index = 0
        self.rocks = rocks
        if rocks == None:
            self.rocks = [MinRock, PlusRock, LRock, IRock, SquareRock]
        self.rock_index = 0
        self.height = [0 for _ in range(width)]

    def get_next_jet(self):
        jet = self.jets[self.jet_index]
        self.jet_index += 1
        if self.jet_index == len(self.jets):
            self.jet_index = 0
        return jet

    def get_next_rock(self):
        rock = self.rock[self.rock_index]
        self.rock_index += 1
        if self.rock_index == len(self.rocks):
            self.rocks = 0
        return rock

    def update(self, rock):
        for i in range(len(self.height)):
            self.height[i] = max(self.height[i], rock.max_height[i])

    def simulate(self, rocks=2022):
        for _ in range(rocks):
            r = self.get_next_rock()(left=2, min_height=max(self.height) + 3)
            move = self.get_next_jet()
            while(r.can_move(move)):
                if move != 'v':
                    move = 'v'
                else:
                    move = self.get_next_jet()
            
            self.update(r)
        
        return max(self.height)


def part1(moves):
    start = timer()
    sim = Simulator(moves)
    height = sim.simulate()
    end = timer()

    print(f'In {(end - start)*1000}ms.')
    return height

def part2(lines):
    start = timer()

    end = timer()

    print(f'In {(end - start)*1000}ms.')

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines[0].strip()))
    print("Score for part 2:", part2(lines[0].strip()))

if __name__ == "__main__":
    main()
