import sys
from collections import defaultdict, deque

m = []
for line in sys.stdin:
    m.append(list(line.strip('\r\n')))

delta = [(0, 1), (0, -1), (-1, 0), (1, 0)]
portals = defaultdict(lambda: set())
G = defaultdict(lambda: set())
for i in range(len(m)):
    for j in range(len(m[0])):
        for di, dj in delta:
            try:
                if m[i][j].isupper() and m[i + di][j + dj].isupper() and m[i + 2*di][j + 2*dj] == '.':
                    if m[i][j] == m[i + di][j + dj] == 'A':
                        sr, sc = i + 2*di, j + 2*dj
                    elif m[i][j] == m[i + di][j + dj] == 'Z':
                        er, ec = i + 2*di, j + 2*dj
                    else:
                        portals[m[min(i, i + di)][min(j, j + dj)] + m[max(i, i + di)][max(j, j + dj)]].add((i + 2*di, j + 2*dj))
            except:
                pass
            try:
                if m[i][j] == m[i + di][j + dj] == '.':
                    G[(i, j)].add((i + di, j + dj))
                    G[(i + di, j + dj)].add((i, j))
            except:
                pass
for p in portals:
    for p1 in portals[p]:
        for p2 in portals[p]:
            if p1 != p2:
                G[p1].add(p2)
                G[p2].add(p1)

def simulate(part1, show_path=False):
    q = deque([(0, sr, sc, 0, [])])
    seen = {(sr, sc) + (0,) * (not part1)}
    while q:
        d, r, c, level, path = q.popleft()
        if part1 and (r, c) == (er, ec):
            print('Part 1:', d)
            break
        if not part1 and (r, c) == (er, ec) and level == 0:
            print('Part 2:', d)
            if show_path:
                print(path)
            break
        for rr, cc in G[(r, c)]:
            in_delta = (r - rr, c - cc) in delta
            outer = (r in [2, len(m) - 3] or c in [2, len(m[0]) - 3]) and not in_delta
            inner = (r not in [2, len(m) - 3] and c not in [2, len(m[0]) - 3]) and not in_delta
            dl = [0, 1, -1][2*outer + inner]
            check = (rr, cc) + (level + dl,) * (not part1)
            if level + dl < 0:
                continue
            if check not in seen:
                seen.add(check)
                # show path metadata
                ret = ''
                if outer:
                    ret += 'outer '
                elif inner:
                    ret += 'inner '
                for p in portals:
                    if (rr, cc) in portals[p]:
                        ret += p
                        ret += f' {level + dl}'
                        break
                q.append((d + 1, rr, cc, level + dl, path + [ret] * (outer or inner)))
simulate(True)
simulate(False)