import sys
from collections import defaultdict
sys.setrecursionlimit(10**5)

arr = list(map(int, input().split(','))) + [0] * 10000

def extract(opcode):
    a, b, c, de = opcode % 100000 // 10000, opcode % 10000 // 1000, opcode % 1000 // 100, opcode % 100
    return a, b, c, de

def intcode(arr, inp):
    inp.reverse()
    pos = 0
    base = 0
    output = []
    while True:
        a, b, c, de = extract(arr[pos])
        if de == 99:
            return output
        elif de == 1:
            arr[arr[pos + 3] + base * (a // 2)] = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]) + (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)])
            pos += 4
        elif de == 2:
            arr[arr[pos + 3] + base * (a // 2)] = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]) * (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)])
            pos += 4
        elif de == 3:
            try:
                arr[arr[pos + 1] + base * (c // 2)] = inp.pop()
            except:
                return output
            pos += 2
        elif de == 4:
            res = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)])
            output.append(res)
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

G = defaultdict(lambda: '.')
config = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}
seen = set()
final_path = []
def spread(moves):
    global found, final_path
    for move in [1, 2, 3, 4]:
        x, y = 0, 0
        output = intcode(arr.copy(), moves + [move])
        path = []
        for i in range(len(output)):
            dx, dy = config[(moves + [move])[i]]
            path.append((x, y))
            if output[i] != 0:
                x += dx
                y += dy
                if output[i] == 2:
                    final_path.append([path, moves, x - dx, y - dy]) # moves is just a metadata
            else:
                G[(x + dx, y + dy)] = '#'
        path.append((x, y))
        path2 = tuple(sorted(set(path)))
        if output[-1] != 0 and path2 not in seen:
            seen.add(path2)
            spread(moves + [move])

spread([])
xo, yo = final_path[0][-2:]
print('Part 1:', len(final_path[0][1]) + 1)
xmin, xmax = min(map(lambda x: x[0], G)), max(map(lambda x: x[0], G))
ymin, ymax = min(map(lambda x: x[1], G)), max(map(lambda x: x[1], G))

def draw(graph):
    for y in range(ymax - ymin + 1):
        for x in range(xmax - xmin + 1):
            if x + xmin == ymax - y == 0:
                print('\033[91mX\033[0m', end='')
            elif x + xmin == xo and ymax - y == yo:
                print('\033[92mO\033[0m', end='')
            elif graph[(x + xmin, ymax - y)] == '#':
                print('\033[94m#\033[0m', end='')
            else:
                print(graph[(x + xmin, ymax - y)], end='')
        print()
    print()

oxy = {}
def fill(x=0, y=0, t=1):
    oxy[(x, y)] = t
    for dx, dy in config.values():
        if xmin <= x + dx <= xmax and ymin <= y + dy <= ymax and G[(x + dx, y + dy)] == '.':
            G[(x + dx, y + dy)] = 'O'
            fill(x + dx, y + dy, t + 1)
fill(xo, yo)
#draw(G)
print('Part 2:', max(oxy.values()))