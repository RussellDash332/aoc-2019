import sys, time
from math import ceil
from collections import defaultdict

need = {}
for line in sys.stdin:
    left, right = line.strip().split(' => ')
    qty, item = right.split()
    need[item] = [int(qty), list(map(lambda x: (x.split()[1], int(x.split()[0])), left.split(', ')))]

ores = 0
spare = defaultdict(lambda: 0)
def breakit(component, qty):
    global ores
    if component == 'ORE':
        ores += qty
        return
    num_rx = ceil((qty) / need[component][0])
    spare[component] = num_rx * need[component][0] - qty
    for c, q in need[component][1]:
        breakit(c, num_rx * q - spare[c])

breakit('FUEL', 1)
ofo = ores
print('Part 1:', ores)

estimate = int(1000000000000 / ofo)
while True:
    spare = defaultdict(lambda: 0)
    ores = 0
    breakit('FUEL', estimate)
    estimate2 = int(1000000000000 / ores * estimate)
    if estimate2 == estimate:
        print('Part 2:', estimate)
        break
    estimate = estimate2