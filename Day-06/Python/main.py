import sys

par = {}
for line in sys.stdin:
    a, b = line.strip().split(')')
    par[b] = a
objs = set(par.keys()) | set(par.values())

orbits = 0
for obj in objs:
    c = 0
    while obj in par:
        c += 1
        obj = par[obj]
    orbits += c
print('Part 1:', orbits)

src, dst = par['YOU'], par['SAN']
sp, dp = [], []
while src in par:
    sp.append(src)
    src = par[src]
while dst in par:
    dp.append(dst)
    dst = par[dst]
def p2():
    for i in range(len(sp)):
        for j in range(len(dp)):
            if sp[i] == dp[j]:
                print('Part 2:', i + j)
                return
p2()