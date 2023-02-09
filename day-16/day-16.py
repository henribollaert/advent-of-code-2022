import os
from timeit import default_timer as timer
from collections import deque

def get_value(s):
    return int(s.strip(';').split('=')[-1])

class Valve:
    def __init__(self, name, flow_rate, neighbours=None) -> None:
        self.name = name
        self.flow_rate = flow_rate
        if neighbours == None:
            self. neighbours = []
        else: 
            self.neighbours = neighbours

    def __str__(self) -> str:
        return f"Valve {self.name} has flow rate={self.flow_rate};" \
         f"tunnels lead to valves {[valve.name for valve in self.neighbours]}"

    def __repr__(self) -> str:
        return f"V-{self.name}"

def parse(lines):
    valves = {}
    for line in lines:
        words=line.split()
        name = words[1]
        neighbours = [n.strip(',') for n in words[9:]]
        if name in valves.keys():
            valves[name].flow_rate = get_value(words[4])
        else:
            valves[name] = Valve(name, get_value(words[4]))
        for neighbour in neighbours:
            if neighbour not in valves.keys():
                valves[neighbour] = Valve(neighbour, None)
            valves[name].neighbours.append(valves[neighbour])
    return valves['AA'], list(valves.values())
            
# we can take 30 actions: each one a move or an opening of a valve
# we will never open a valve with flow rate 1
# after we have opened a valve, we can immediately look for the next best valve
# !!!! This is a greedy strategy
# how do we define that: total added released pressure from that time:
# flow_rate * (remainging_time - distance - 1)
# we can check this with back_tracking
# let's calculate all pairwise distances first

def pairwise_distances(valves):
    distances = {}
    for valve in valves:
        d_v = {valve : 0}
        q = deque([valve])
        while len(q) > 0:
            v = q.popleft()
            for w in v.neighbours:
                if w not in d_v.keys():
                    d_v[w] = d_v[v] + 1
                    q.append(w)
        distances[valve] = d_v
    return distances

best_max = 0
distances = None

# the only possible paths go to unopened valves

def recurse(cur_valve:Valve,
            total_pressure:int,
            time_remaining:int,
            opened_valves:dict):

    global best_max
    
    if total_pressure + max(0, time_remaining)*max_added <= best_max:
        # print('a')
        return 0
        # print(total_pressure)
        # best_max = max(best_max, total_pressure)
        # return total_pressure

    ppm = sum([valve.flow_rate for valve, opened in opened_valves.items() if opened])
    if all(opened_valves.values()):
        total = total_pressure + max(0, time_remaining) * ppm
        best_max = max(total, best_max)
        return total
    max_total = 0 
    for possible_next, opened in opened_valves.items():
        if not opened:
            travel_time = distances[cur_valve][possible_next] + 1  # travel and opening time
            if travel_time < time_remaining:
                opened_valves[possible_next] = True
                max_total = max(max_total,
                            recurse(possible_next,
                                    total_pressure + travel_time*ppm,
                                    time_remaining - travel_time,
                                    opened_valves))
                opened_valves[possible_next] = False
            else:
                max_total = max(max_total, total_pressure + time_remaining * ppm)
    best_max = max(best_max, max_total)
    return max_total

def greedy_bound(t, dist, remaining):
    return t.flow_rate * (remaining - dist - 1)

def greedy(start, to_open):
    cur = start
    remaining = 30
    opened = {v: False for v in to_open}
    total = 0
    while not all(opened.values()) and remaining > 0:
        best = 0
        best_next = None
        for next in [valve for valve, o in opened.items() if not o]:
            val = greedy_bound(next, distances[cur][next], remaining)
            if val > best:
                best = val
                best_next = next
            if best == 0:
                return total + remaining * sum([k.flow_rate for k, v in opened.items() if v])
        elapsed = 1 + distances[cur][best_next]
        total += elapsed * sum([k.flow_rate for k, v in opened.items() if v])
        remaining -= (elapsed)
        cur = best_next
        opened[cur] = True
    return total


def part1(lines):
    start_valve, valves = parse(lines)

    start = timer()
    valves_to_open = [valve for valve in valves if valve.flow_rate > 0]
    global max_added, best_max, distances
    max_added = sum([v.flow_rate for v in valves_to_open])
    distances = pairwise_distances(valves)
    best_max = greedy(start_valve, valves_to_open)
    res = recurse(start_valve, 0, 30, {v: False for v in valves_to_open} )

    end = timer()

    print(f'In {(end - start)*1000}ms.')
    return res

# def find_target(cur_valve, time_remaining, opened_valves):
    

# def recurse2(my_valve:Valve,
#              el_valve:Valve,
#              total_pressure:int,
#              time_remaining:int,
#              opened_valves:dict):
#     global best_max
    
#     if total_pressure + max(0, time_remaining)*max_added <= best_max:
#         return 0

#     ppm = sum([valve.flow_rate for valve, opened in opened_valves.items() if opened])

#     if all(opened_valves.values()):
#         total = total_pressure + max(0, time_remaining) * ppm
#         best_max = max(total, best_max)
#         return total

    
#     max_total = 0
#     for possible_next, opened in opened_valves.items():
#         if not opened:
#             travel_time = distances[cur_valve][possible_next] + 1  # travel and opening time
#             if travel_time < time_remaining:
#                 opened_valves[possible_next] = True
#                 max_total = max(max_total,
#                             recurse(possible_next,
#                                     total_pressure + travel_time*ppm,
#                                     time_remaining - travel_time,
#                                     opened_valves))
#                 opened_valves[possible_next] = False
#             else:
#                 max_total = max(max_total, total_pressure + time_remaining * ppm)
#     best_max = max(best_max, max_total)
#     return max_total

def part2(lines):  # should be run after part 1

    start_valve, valves = parse(lines)

    start = timer()
    valves_to_open = [valve for valve in valves if valve.flow_rate > 0]
    print(valves_to_open)
    # res = recurse2(start_valve, start_valve, 0, 26, {v: False for v in valves_to_open})


    end = timer()

    print(f'In {(end - start)*1000}ms.')

def main():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, 'input-16.txt'), 'r')
    lines = f.readlines()
    f.close()
    
    print("Score for part 1:", part1(lines))
    print("Score for part 2:", part2(lines))

if __name__ == "__main__":
    main()
