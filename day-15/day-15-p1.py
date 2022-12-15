
def manhattan_distance(x, y):
    return sum([abs(c_x - c_y) for c_x, c_y in zip(x, y)])

# i guess we have to be smart and not use a cave map

class CaveMap:
    def __init__(self, min_row, max_row, min_col, max_col) -> None:
        self.cave_map = [['.' for _ in range(min_col, max_col+1)] for _ in range(min_row, max_row + 1)]
        self.row_offset = min_row
        self.column_offset = min_col
        self.num_rows = max_row + 1 - min_row
        self.num_cols = max_col + 1 - min_col

    def put(self, s, row, col):
        self.cave_map[row - self.row_offset][col - self.column_offset] = s

    def get(self, row, col):
        return self.cave_map[row - self.row_offset][col - self.column_offset]        

    def fill(self, sensor):
        self.put('S', sensor.row, sensor.col)
        self.put('B', sensor.beacon_row, sensor.beacon_col)
        for row in range(sensor.get_range() + 1):
            for col in range(sensor.get_range() - row + 1):
                if self.get(sensor.row - row, sensor.col - col) == '.':
                    self.put('#', sensor.row - row, sensor.col - col)
                if self.get(sensor.row - row, sensor.col + col) == '.':
                    self.put('#', sensor.row - row, sensor.col + col)
                if self.get(sensor.row + row, sensor.col - col) == '.':
                    self.put('#', sensor.row + row, sensor.col - col)
                if self.get(sensor.row + row, sensor.col + col) == '.':
                    self.put('#', sensor.row + row, sensor.col + col)

    def check_row(self, row):
        not_present = 0
        for col in range(self.num_cols):
            if self.cave_map[row - self.row_offset][col] == '#':
                not_present += 1
        return not_present

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

def part1_slow(lines, row_of_interest=10):
    sensors = parse(lines)
    min_column = max_column = min_row = max_row = 0
    for sensor in sensors:
        min_row = min(min_row, sensor.row - sensor.get_range(), sensor.beacon_row)
        max_row = max(max_row, sensor.row + sensor.get_range(), sensor.beacon_row)
        min_column = min(min_column, sensor.col - sensor.get_range() , sensor.beacon_col)
        max_column = max(max_column, sensor.col + sensor.get_range(), sensor.beacon_col)
    cave_map = CaveMap(min_row, max_row, min_column, max_column)
    for sensor in sensors:
        cave_map.fill(sensor)


    print("".join(cave_map.cave_map[row_of_interest - cave_map.row_offset]))
    
    return cave_map.check_row(row_of_interest)