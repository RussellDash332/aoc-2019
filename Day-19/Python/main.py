arr = list(map(int, input().split(','))) + [0] * 10000

def extract(opcode):
    a, b, c, de = opcode % 100000 // 10000, opcode % 10000 // 1000, opcode % 1000 // 100, opcode % 100
    return a, b, c, de

def intcode(arr, inp=[]):
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
            arr[arr[pos + 1] + base * (c // 2)] = inp.pop()
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

def draw(m):
    def count_tags(x):
        return x.count('#') + x.count('\033[91m#\033[0m'), x.count('\033[91m#\033[0m') 
    print('\n'.join(map(lambda x: f"{''.join(x)} {count_tags(x)}", m))+'\n')

def simulate(endx, endy, startx=0, starty=0, highlight=None):
    affected = 0
    m = []
    for x in range(startx, endx):
        m.append([])
        for y in range(starty, endy):
            res = intcode(arr.copy(), [x, y])[0]
            affected += res
            if not highlight:
                m[-1].append(['.', '#'][res])
            elif highlight[0] <= x < highlight[0] + 100 and highlight[1] <= y < highlight[1] + 100:
                m[-1].append(['.', '\033[91m#\033[0m'][res])
            else:
                m[-1].append(['.', '#'][res])
    return affected, m
print('Part 1:', simulate(50, 50)[0])

def visualize(debug=True):
    cx, cy = 1353, 701
    highlight = (cx, cy + 63)
    if debug:
        print(cx, cy)
        print('Highlight:', highlight, '-', tuple(map(lambda x: x + 100, highlight)))
        draw(simulate(cx + 100, cy + 200, cx, cy, highlight)[1])
    return highlight
hx, hy = visualize(False)
print('Part 2:', hx * 10000 + hy)