import os
from timeit import default_timer as timer


def manhattan_distance(x, y):
    return sum([abs(c_x - c_y) for c_x, c_y in zip(x, y)])

class Sensor:
    def __init__(self, location, closest_beacon) -> None:
        self.col, self.row = location
        self.beacon_col, self.beacon_row = closest_beacon
        self.range = manhattan_distance((self.row, self.col), (self.beacon_row, self.beacon_col))

    def get_range(self):
        return self.range

    def __str__(self) -> str:
        return f"Sensor at x={self.col}, y={self.row}:" \
               f"closest beacon is at x={self.beacon_col}, y={self.beacon_row}"


def get_value(s):
    return int(s.strip(':,\n').split('=')[-1])

def parse(lines):
    sensors = []
    for line in lines:
        parts = line.split()
        sensors.append(Sensor((get_value(parts[2]), get_value(parts[3])),
                              (get_value(parts[-2]), get_value(parts[-1]))))
    return sensors

def part1(lines, row_of_interest):
    sensors = parse(lines)
    start = timer()
    occupied_slots = set()
    for sensor in sensors:
        for i in range(sensor.get_range()  - abs(sensor.row - row_of_interest)+ 1):
            occupied_slots.add(sensor.col - i)
            occupied_slots.add(sensor.col + i)
    for sensor in sensors:
        if sensor.row == row_of_interest and sensor.col in occupied_slots:
            occupied_slots.remove(sensor.col)
        if sensor.beacon_row == row_of_interest and sensor.beacon_col in occupied_slots:
            occupied_slots.remove(sensor.beacon_col)
    end = timer()
    print(f"In {end-start}s")

    return len(occupied_slots)  

# with a hint from Charlotte, way faster
def part1_with_intervals(lines, row_of_interest):
    sensors = parse(lines)
    start = timer()
    smallest = largest = 0
    for sensor in sensors:
        smallest = min(smallest, sensor.col - (sensor.get_range()  - abs(sensor.row - row_of_interest)))
        largest = max(largest, sensor.col + (sensor.get_range()  - abs(sensor.row - row_of_interest)))
    for sensor in sensors:
        taken = set()
        if sensor.row == row_of_interest and smallest <= sensor.col <= largest:
            taken.add(sensor.col)
        if sensor.beacon_row == row_of_interest and smallest <= sensor.beacon_col <= largest:
            taken.add(sensor.beacon_col)
    res = largest - smallest - len(taken)
    end = timer()
    print(f"In {(end-start)*1000}ms")

    return res


def get_intersection(a, b):
    return ((b+a)//2, (b-a)//2)

# we have to compress the search space somehow
# if the missing sensor is not on the boundary of the square, it must be on an intersection
# of the boundaries of at least 2 scanners
# those boundaries are defined by 4 lines and we can easily calculate them
def part2supersmart(lines, limit, factor=4000000):
    sensors = parse(lines)
    start = timer()
    possible = []
    for i, sensor1 in enumerate(sensors):
        a1 = [sensor1.row - sensor1.col + sensor1.range + 1,
              sensor1.row - sensor1.col - sensor1.range - 1]
        b1 = [sensor1.row + sensor1.col + sensor1.range + 1,
              sensor1.row + sensor1.col - sensor1.range - 1]
        for sensor2 in sensors[i+1:]:
            a2 = [sensor2.row - sensor2.col + sensor2.range + 1,
                  sensor2.row - sensor2.col - sensor2.range - 1]
            b2 = [sensor2.row + sensor2.col + sensor2.range + 1,
                  sensor2.row + sensor2.col - sensor2.range - 1]
            for a in range(2):
                for b in range(2):
                    possible.append(get_intersection(a1[a], b2[b]))
                    possible.append(get_intersection(a2[a], b1[b]))
    for row, col in possible:
        if 0 <= row <= limit and 0 <= col <= limit and \
        not any([manhattan_distance((sensor.row, sensor.col),(row, col)) <= sensor.range for sensor in sensors]):
            end = timer()
            print(f"In {(end-start)*1000}ms:")
            return row + col * factor              

# my smartest solution: checking all points on the boundary lines
def part2(lines, limit, factor=4000000):
    sensors = parse(lines)
    possible = []
    for sensor in sensors:
        r = sensor.get_range()
        for i in range(r):
            if sensor.col + i <= limit and sensor.row + r + 1 -i <= limit:
                possible.append((sensor.row + r + 1 -i, sensor.col + i))
            if sensor.col + r + 1 - i <= limit and sensor.row - i >= 0:
                possible.append((sensor.row - i, sensor.col + r + 1 - i))
            if sensor.col - i >= 0 and sensor.row - r - 1 + i >= 0:
                possible.append((sensor.row - r - 1 + i, sensor.col - i))
            if sensor.col - r - 1 + i >= 0 and sensor.row + i <= limit:
                possible.append((sensor.row + i, sensor.col - r - 1 + i))
    for row, col in possible:
        if not any([manhattan_distance((sensor.row, sensor.col),(row, col)) <= sensor.range for sensor in sensors]):
                return row + col * factor

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-15.txt'), 'r')
    lines = f.readlines()
    f.close()

    print("Score for part 1:", part1_with_intervals(lines, row_of_interest=2000000)) # 2000000 or 10
    # print('This might take a while')
    # print("Score for part 2:", part2(lines, limit=4000000))
    print("Score for part 2:", part2supersmart(lines, limit=4000000))

if __name__ == "__main__":
    main()
