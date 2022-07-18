import sys
from math import atan2, pi
from copy import deepcopy

m = []
for line in sys.stdin:
    m.append(list(line.strip()))

meteors = []
for r in range(len(m)):
    for c in range(len(m[0])):
        if m[r][c] == '#':
            meteors.append((r, c))

def scan(pos, m=m):
    rx, cx = pos
    if m[rx][cx] != '#':
        return {}
    meteors = []
    for r in range(len(m)):
        for c in range(len(m[0])):
            if m[r][c] == '#' and not (r - rx == c - cx == 0):
                meteors.append((c - cx, r - rx))
    meteors.sort(key=lambda x: [atan2(*x), sum(map(abs, x))])
    seen = {}
    for met in meteors:
        if atan2(*met) not in seen:
            seen[atan2(*met)] = met
    return seen

def scan2(pos):
    return len(scan(pos))

def vaporize(pos, nth):
    m2 = deepcopy(m)
    rx, cx = pos
    vap = []
    while len(vap) <= nth:
        on_sight = sorted(scan(pos, m2).values(), key=lambda x: pi-atan2(*x))
        for dc, dr in on_sight:
            dest = (rx + dr, cx + dc)
            m2[dest[0]][dest[1]] = '.'
            vap.append(dest)
    rv, cv = vap[nth - 1]
    return 100*cv + rv

best = max(meteors, key=scan2)
print('Part 1:', scan2(best))
print('Part 2:', vaporize(best, 200))