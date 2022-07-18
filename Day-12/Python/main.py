import re, sys
from copy import deepcopy

def gcd(a,b):
    while b: a,b = b,a%b
    return a
    
def lcm(a,b):
    return a*b//gcd(a,b)

moons = []
for line in sys.stdin:
    moons.append(list(map(int, re.findall('[-\d]+', line))))
moons2 = deepcopy(moons)
mx, my, mz = [[m[i] for m in moons2] for i in range(3)]

seen = set()
vv = [[0, 0, 0] for _ in moons]
for _ in range(1000):
    for i, m1 in enumerate(moons):
        for m2 in moons:
            if m1 != m2:
                for j in range(3):
                    if m1[j] == m2[j]:
                        continue
                    vv[i][j] += 2*(m1[j] < m2[j]) - 1
    for i in range(len(moons)):
        for j in range(3):
            moons[i][j] += vv[i][j]
print('Part 1:', sum(map(lambda x: sum(map(abs, moons[x])) * sum(map(abs, vv[x])), range(len(moons)))))

cycle = []
vv = [[0, 0, 0] for _ in moons]
for i, mm in enumerate([mx, my, mz]):
    check, step = mm.copy(), 0
    while True:
        step += 1
        for j, m1 in enumerate(mm):
            for k, m2 in enumerate(mm):
                if j != k:
                    if m1 == m2:
                        continue
                    vv[j][i] += 2*(m1 < m2) - 1
        for j in range(len(mm)):
            mm[j] += vv[j][i]
        if mm == check and vv[i] == [0, 0, 0]:
            cycle.append(step)
            break
ans = 1
for c in cycle:
    ans = lcm(ans, c)
print('Part 2:', ans)