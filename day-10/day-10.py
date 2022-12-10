import os

# addx V: adds V to the value in register X after 2 cycles
# i.e. during the 2 cycles, the value remains unchanged

CYCLES_OF_INTEREST = [20, 60, 100, 140, 180, 220]
ADDX_LENGTH = 2
DISPLAY_HEIGHT = 6
DISPLAY_WIDTH = 40

class CPU:
    def __init__(self, verbose = False) -> None:
        self.reg_x = 1
        self.cycle = 1
        self.verbose = verbose
        self.interesting_values = dict()
        self.display = []
    
    def get_signal_strength(self):
        return self.reg_x * self.cycle

    def tick(self):
        if self.cycle in CYCLES_OF_INTEREST:
            if self.verbose:
                print(f"During cycle {self.cycle}, signal strength is {self.get_signal_strength()}.")
            self.interesting_values[self.cycle]= self.get_signal_strength()
        self.cycle += 1
    
    def addx(self, v):
        self.reg_x += v

    def draw(self):
        cur = (self.cycle - 1) % DISPLAY_WIDTH
        self.cycle += 1
        if abs(cur - self.reg_x) <= 1:
            self.display.append('#')
        else:
            self.display.append('.')
            


def get_instructions(lines):
    return [line.split() for line in lines]
        

def part1(lines):
    cpu = CPU()
    for instruction in get_instructions(lines):
        # print(instruction)
        if instruction[0] == 'noop':
            cpu.tick()
        else:
            for _ in range(ADDX_LENGTH):
                cpu.tick()
            cpu.addx(int(instruction[1]))
    return sum([val for key, val in cpu.interesting_values.items()])

def part2(lines):
    cpu = CPU()
    for instruction in get_instructions(lines):
        if instruction[0] == 'noop':
            cpu.draw()
        else:
            for _ in range(ADDX_LENGTH):
                cpu.draw()
            cpu.addx(int(instruction[1]))
    for row in range(DISPLAY_HEIGHT):
        print("".join(cpu.display[row*DISPLAY_WIDTH:(row+1)*DISPLAY_WIDTH]))
    return "See above"


def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-10.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))

if __name__ == "__main__":
    main()