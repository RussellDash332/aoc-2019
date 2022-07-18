from collections import defaultdict
arr = list(map(int, input().split(','))) + [0] * 10000

def extract(opcode):
    a, b, c, de = opcode % 100000 // 10000, opcode % 10000 // 1000, opcode % 1000 // 100, opcode % 100
    return a, b, c, de

panel = defaultdict(lambda: 0)
panel2 = defaultdict(lambda: 0)
panel2[(0, 0)] = 1

def intcode(arr, panel):
    painted = set()
    pos = 0
    base = 0
    x, y, dx, dy = 0, 0, 0, 1
    paint = True
    while True:
        a, b, c, de = extract(arr[pos])
        if de == 99:
            return len(painted)
        elif de == 1:
            arr[arr[pos + 3] + base * (a // 2)] = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]) + (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)])
            pos += 4
        elif de == 2:
            arr[arr[pos + 3] + base * (a // 2)] = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]) * (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)])
            pos += 4
        elif de == 3:
            arr[arr[pos + 1] + base * (c // 2)] = panel[(x, y)]
            pos += 2
        elif de == 4:
            res = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)])
            if paint:
                panel[(x, y)] = res
                painted.add((x, y))
            else:
                dx, dy = [(-dy, dx), (dy, -dx)][res]
                x += dx
                y += dy
            paint = not paint
            pos += 2
        elif de == 5:
            if (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]):
                pos = (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)])
            else:
                pos += 3
        elif de == 6:
            if not (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]):
                pos = (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)])
            else:
                pos += 3
        elif de == 7:
            arr[arr[pos + 3] + base * (a // 2)] = int((arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]) < (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)]))
            pos += 4
        elif de == 8:
            arr[arr[pos + 3] + base * (a // 2)] = int((arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]) == (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)]))
            pos += 4
        elif de == 9:
            base += (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)])
            pos += 2
        else:
            pos += 1

print('Part 1:', intcode(arr.copy(), panel))
intcode(arr.copy(), panel2)
print('Part 2:')
xmin, xmax = min(map(lambda x: x[0], panel2)), max(map(lambda x: x[0], panel2))
ymin, ymax = min(map(lambda x: x[1], panel2)), max(map(lambda x: x[1], panel2))
for y in range(ymax - ymin + 1):
    for x in range(xmax - xmin + 1):
        print('.#'[panel2[(x + xmin, ymax - y)]], end='')
    print()