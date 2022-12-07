import os
from abc import ABC, abstractmethod
import re

class Item (ABC):

    OFFSET = '  '

    def __init__(self, name, parent, level = None) -> None:
        self.name = name
        self.parent = parent
        if level == None:
            self.level = parent.level + 1
        else:
            self.level = level
    
    @abstractmethod
    def get_size(self) -> int:
        pass

    def get_name(self) -> str:
        return self.name

    def get_parent(self):
        return self.parent

    def get_string(self):
        return Item.OFFSET * self.level + f"{self.get_name()} (size = {self.get_size()})"

    def print(self):
        print(self.get_string())

class Directory(Item):
    def __init__(self, name, parent, level=None) -> None:
        super().__init__(name, parent, level)
        self.subitems = []

    def add_item(self, item: Item):
        self.subitems.append(item)

    def get_size(self) -> int:
        return sum([i.get_size() for i in self.subitems])

    def get_name(self) -> str:
        return "(dir) " + super().get_name()

    def print(self):
        print(self.get_string())
        for item in self.subitems:
            item.print()
        print(Item.OFFSET * self.level + "end of " + self.get_name())
    
class File(Item):
    def __init__(self, name: str, parent: Directory, size: int, level=None) -> None:
        super().__init__(name, parent, level)
        self.size = size

    def get_size(self) -> int:
        return self.size


def parse(lines) -> Directory:
    top_dir = Directory('TOP', None, level=0)
    super_dir = top_dir
    for line in lines:
        words = line.split()
        if words[1] == 'cd':
            if words[2] == '..':
                super_dir = super_dir.get_parent()
            else:
                new_dir = Directory(words[2], super_dir)
                super_dir.add_item(new_dir)
                super_dir = new_dir
        elif re.search("\d", words[0]):
            super_dir.add_item(File(words[1], super_dir, int(words[0])))

    return top_dir.subitems[0]



def find(top_dir, atmost = True, limit = 100000):
    result = []
    dirs = [top_dir]
    while len(dirs) > 0:
        cur = dirs.pop()
        for d in cur.subitems:
            if isinstance(d, Directory):
                dirs.append(d)
        if (cur.get_size() < limit) == atmost or cur.get_size() == limit:
            result.append(cur)
    return result


def part1(lines):
    return sum([d.get_size() for d in find(parse(lines))])

TOTAL_SPACE = 70000000
REQUIRED_SPACE = 30000000

def part2(lines):
    top_dir = parse(lines)
    limit = REQUIRED_SPACE - (TOTAL_SPACE - top_dir.get_size())
    return min([d.get_size() for d in find(top_dir=top_dir, atmost=False, limit=limit)])

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-7.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Size for part 1:", part1(lines))
    print("Size for part 2:", part2(lines))

if __name__ == "__main__":
    main()
