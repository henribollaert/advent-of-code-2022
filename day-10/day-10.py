import os
from abc import ABC, abstractmethod

class CPU(ABC):
    def __init__(self, addx_length = 2, verbose = False) -> None:
        self.reg_x = 1
        self.cycle = 1
        self.addx_length = addx_length
        self.verbose = verbose
    
    def get_signal_strength(self):
        return self.reg_x * self.cycle

    @abstractmethod
    def tick(self):
        """
        Should specifiy what happens when a cycle passes, including any checks or drawing.
        """
        pass

    def noop(self):
        """
        Skips 1 cycle
        """
        self.tick()
    
    def addx(self, v):
        """
        Adds V to the value in register X after 2 cycles, i.e.,
        during the 2 cycles, the value remains unchanged.
        """
        for _ in range(self.addx_length):
            self.tick()
        self.reg_x += v


class TickingCPU(CPU):
    def __init__(self, interesting_freq = 40, interesting_offset = 20, addx_length = 2, verbose=False) -> None:
        super().__init__(addx_length, verbose)
        self.interesting_freq = interesting_freq
        self.interesting_offset = interesting_offset
        self.interesting_values = dict()

    def tick(self):
        if self.cycle % self.interesting_freq == self.interesting_offset:
            if self.verbose:
                print(f"During cycle {self.cycle}, signal strength is {self.get_signal_strength()}.")
            self.interesting_values[self.cycle]= self.get_signal_strength()
        self.cycle += 1

    def get_combined_signal_strength(self):
        return sum([val for key, val in self.interesting_values.items()])

    
class DrawingCPU(CPU):
    def __init__(self, on_char = '#', off_char = '.', display_width = 40, display_height = 6, addx_length = 2, verbose=False) -> None:
        super().__init__(addx_length, verbose)
        self.display = []
        self.on_char = on_char
        self.off_char = off_char
        self.display_width = display_width
        self.display_height = display_height

    def tick(self):
        cur = (self.cycle - 1) % self.display_width
        self.cycle += 1
        if abs(cur - self.reg_x) <= 1:
             self.display.append(self.on_char)
        else:
            self.display.append(self.off_char)

    def get_display_string(self):
        s = "\n"
        for row in range(self.display_height):
            s += "".join(self.display[row*self.display_width:(row+1)*self.display_width]) + "\n"
        return s
            

def get_instructions(lines):
    return [line.split() for line in lines]

def run_cpu(cpu:CPU, instructions):
    for instruction in instructions:
        if instruction[0] == 'noop':
            cpu.noop()
        else:
            cpu.addx(int(instruction[1]))
        

def part1(lines):
    cpu = TickingCPU()
    run_cpu(cpu, get_instructions(lines))
    return cpu.get_combined_signal_strength()

def part2(lines):
    cpu = DrawingCPU()
    run_cpu(cpu, get_instructions(lines))
    return cpu.get_display_string()


def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-10.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Combined signal strength for part 1:", part1(lines))
    print("Display for part 2:", part2(lines))

if __name__ == "__main__":
    main()