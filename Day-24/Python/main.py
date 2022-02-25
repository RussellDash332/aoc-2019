import sys

def empty_grid():
    m = []
    for _ in range(5):
        m.append(['.'] * 5)
    return m

m, m2 = [], []
look = set()
for line in sys.stdin:
    m.append(list(line.strip()))
    m2.append(list(line.strip()))

while tuple(map(tuple, m)) not in look:
    new_m = empty_grid()
    for i in range(5):
        for j in range(5):
            if m[i][j] == '.':
                check = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if abs(di) + abs(dj) == 1 and 0 <= i + di < 5 and 0 <= j + dj < 5:
                            check += int(m[i + di][j + dj] == '#')
                new_m[i][j] = ['.', '#'][int(check in [1, 2])]
            else:
                check = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if abs(di) + abs(dj) == 1 and 0 <= i + di < 5 and 0 <= j + dj < 5:
                            check += int(m[i + di][j + dj] == '#')
                new_m[i][j] = ['.', '#'][int(check == 1)]
    look.add(tuple(map(tuple, m)))
    m = new_m

bd = 0
for i in range(5):
    for j in range(5):
        bd += int(m[i][j] == '#') * 2**(5 * i + j)
print('Part 1:', bd)

H = {0: {}} # depth -> grid
for i in range(5):
    for j in range(5):
        if (i, j) != (2, 2):
            H[0][(i, j)] = m2[i][j]

for t in range(200):
    new_H = {}
    hk = list(H.keys())
    for d in hk + [max(hk) + 1, min(hk) - 1]:
        for i, j in H.get(d, [(a, b) for a in range(5) for b in range(5) if (a, b) != (2, 2)]):
            if i in [1, 3] and j in [1, 3]:
                check = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if abs(di) + abs(dj) == 1 and H.get(d, {}).get((i + di, j + dj), '.') == '#':
                            check += 1
            elif i in [0, 4] and j in [1, 2, 3]:
                check = 0
                for di in [0, [1, -1][i // 4]]:
                    for dj in [-1, 0, 1]:
                        if abs(di) + abs(dj) == 1 and H.get(d, {}).get((i + di, j + dj), '.') == '#':
                            check += 1
                check += H.get(d - 1, {}).get(([1, 3][i // 4], 2), '.') == '#'
            elif j in [0, 4] and i in [1, 2, 3]:
                check = 0
                for dj in [0, [1, -1][j // 4]]:
                    for di in [-1, 0, 1]:
                        if abs(di) + abs(dj) == 1 and H.get(d, {}).get((i + di, j + dj), '.') == '#':
                            check += 1
                check += H.get(d - 1, {}).get((2, [1, 3][j // 4]), '.') == '#'
            elif i in [0, 4] and j in [0, 4]:
                check = 0
                for di in [0, [1, -1][i // 4]]:
                    for dj in [0, [1, -1][j // 4]]:
                        if abs(di) + abs(dj) == 1 and H.get(d, {}).get((i + di, j + dj), '.') == '#':
                            check += 1
                check += H.get(d - 1, {}).get((2, [1, 3][j // 4]), '.') == '#'
                check += H.get(d - 1, {}).get(([1, 3][i // 4], 2), '.') == '#'
            else: # i = 2 or j = 2 but not both
                check = 0
                if i == 2: # j = 1 or 3
                    for di in [-1, 0, 1]:
                        for dj in [0, [-1, 1][(j - 1) // 2]]:
                            if abs(di) + abs(dj) == 1 and H.get(d, {}).get((i + di, j + dj), '.') == '#':
                                check += 1
                    for k in range(5):
                        check += H.get(d + 1, {}).get((k, 2*j-2), '.') == '#'
                else: # j == 2, i = 1 or 3
                    for dj in [-1, 0, 1]:
                        for di in [0, [-1, 1][(i - 1) // 2]]:
                            if abs(di) + abs(dj) == 1 and H.get(d, {}).get((i + di, j + dj), '.') == '#':
                                check += 1
                    for k in range(5):
                        check += H.get(d + 1, {}).get((2*i-2, k), '.') == '#'

            if d not in new_H:
                new_H[d] = {}
            if d not in [max(hk) + 1, min(hk) - 1]:
                new_H[d][(i, j)] = ['.', '#'][int((check in [1, 2] and H[d][(i, j)] == '.') or (check == 1 and H[d][(i, j)] == '#'))]
            else:
                new_H[d][(i, j)] = ['.', '#'][int(check in [1, 2])]
    H = new_H
print('Part 2:', sum(map(lambda x: sum(map(lambda y: y == '#', x.values())), H.values())))