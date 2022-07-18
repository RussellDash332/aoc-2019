import sys
from heapq import *
from collections import defaultdict, deque

m = []
for line in sys.stdin:
    m.append(list(line.strip()))

num_keys = 0
delta = [(0, -1), (-1, 0), (0, 1), (1, 0)]
for rr in range(len(m)):
    for cc in range(len(m[0])):
        if m[rr][cc] == '@':
            sr, sc = rr, cc
            m[rr][cc] = '.'
        num_keys += m[rr][cc].islower()

def make_graph(m):
    g = defaultdict(lambda: set())
    for i in range(1, len(m) - 1):
        for j in range(1, len(m[0]) - 1):
            if m[i][j] != '#':
                for di, dj in delta:
                    if m[i + di][j + dj] != '#':
                        g[(i, j)].add((i + di, j + dj))
                        g[(i + di, j + dj)].add((i, j))
    return g

def draw(m):
    print('\n'.join(map(lambda x: ''.join(x).replace('#', '█'), m))+'\n')

def simulate(bots, part):
    g = make_graph(m)

    # Do BFS to scan all keys for each quadrant
    dist = defaultdict(lambda: (1 << num_keys) - 1)
    q = deque([(0, *p, i) for i, p in enumerate(bots)])
    seen = set(bots)
    while q:
        # keep distance as metadata
        d, r, c, i = q.popleft()
        for rr, cc in g[(r, c)]:
            if (rr, cc) not in seen:
                seen.add((rr, cc))
                if m[rr][cc].islower():
                    dist[i] ^= (1 << (ord(m[rr][cc]) - ord('a')))
                q.append((d + 1, rr, cc, i))

    # Dijkstra-ish implementation :)
    def mini_simulate(pos, keys_collected):
        seen = defaultdict(lambda: defaultdict(lambda: float('inf')))
        q = [(0, pos, keys_collected)]
        while q:
            dist, pos, keys = heappop(q)
            if dist >= seen[keys][pos]:
                continue
            seen[keys][pos] = dist
            if keys == (1 << num_keys) - 1:
                return dist
            for r, c in g[pos]:
                if m[r][c] == '.' or (m[r][c].isupper() and (1 << (ord(m[r][c].lower()) - ord('a'))) & keys != 0): # empty space or unlocked door
                    heappush(q, (dist + 1, (r, c), keys))
                elif m[r][c].islower(): # key
                    heappush(q, (dist + 1, (r, c), keys | (1 << (ord(m[r][c].lower()) - ord('a')))))
                # else part is when the door is locked, nothing happens

    ans = 0
    for i, bot in enumerate(bots):
        ans += mini_simulate(bot, dist[i])
    print(f'Part {part}: {ans}')

#draw(m)
simulate([(sr, sc)], 1)
m[sr - 1][sc] = m[sr + 1][sc] = m[sr][sc] = m[sr][sc - 1] = m[sr][sc + 1] = '#'
#draw(m)
simulate([(sr - 1, sc - 1), (sr - 1, sc + 1), (sr + 1, sc - 1), (sr + 1, sc + 1)], 2)