import time
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
            return ''.join(output)
        elif de == 1:
            arr[arr[pos + 3] + base * (a // 2)] = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]) + (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)])
            pos += 4
        elif de == 2:
            arr[arr[pos + 3] + base * (a // 2)] = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]) * (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)])
            pos += 4
        elif de == 3:
            try:
                arr[arr[pos + 1] + base * (c // 2)] = inp.pop()
                #print(chr(arr[arr[pos + 1] + base * (c // 2)]), arr[arr[pos + 1] + base * (c // 2)])
            except:
                return
            pos += 2
        elif de == 4:
            res = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)])
            output.append(chr(res))
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

m = list(map(list, intcode(arr.copy()).strip().split('\n')))
ap = 0
turns = []
for i in range(1, len(m) - 1):
    for j in range(1, len(m[0]) - 1):
        adj = m[i][j] == '#'
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            adj += m[i + di][j + dj] == '#'
        if adj == 5:
            ap += i * j
        elif adj == 3:
            turns.append((i, j))
print('Part 1:', ap)

debug = False
for i in range(len(m)):
    for j in range(len(m[0])):
        if m[i][j] in '^<v>':
            k = '^<v>'.index(m[i][j])
            br, bc = i, j
            vr, vc = [-1, 0, 1, 0][k], [0, -1, 0, 1][k]
moves = []
dust = set()
prevr, prevc = None, None
while True:
    possible = False
    for dr, dc in [(vr, vc), (-vc, vr), (vc, -vr), (-vr, vc)]:
        if 0 <= br + dr < len(m) and 0 <= bc + dc < len(m[0]):
            if '#' in m[br + dr][bc + dc] and (br + dr, bc + dc) != (prevr, prevc):
                dust.add((br + dr, bc + dc))
                m[br + dr][bc + dc] = '\033[91m#\033[0m'
                possible = True
                if (dr, dc) == (-vc, vr):
                    moves.append('L')
                    moves.append(1)
                elif (dr, dc) == (vc, -vr):
                    moves.append('R')
                    moves.append(1)
                else: # dr, dc == vr, vc; opposite case never happen
                    moves[-1] += 1
                prevr, prevc = br, bc
                br += dr
                bc += dc
                vr, vc = dr, dc
                break
    if not possible:
        break
    if debug:
        print('\n'.join(map(''.join, m))+'\n')
        time.sleep(0.05)

# L,4,L,4,L,10,R,4          -> A
#   R,4,L,4,L,4,R,8,R,10    -> B
# L,4,L,4,L,10,R,4          -> A
#       R,4,L,10,R,10       -> C
# L,4,L,4,L,10,R,4          -> A
#       R,4,L,10,R,10       -> C
#   R,4,L,4,L,4,R,8,R,10    -> B
#       R,4,L,10,R,10       -> C
#       R,10,L,10,R,10      -> C
#   R,4,L,4,L,4,R,8,R,10    -> B
#print(','.join(map(str, moves)))

def trans(txt):
    return list(map(ord, txt)) + [10]

main = 'A,B,A,C,A,C,B,C,C,B'
A = 'L,4,L,4,L,10,R,4'
B = 'R,4,L,4,L,4,R,8,R,10'
C = 'R,4,L,10,R,10'
continuous = 'n'
m = list(map(list, intcode([2] + arr[1:], trans(main) + trans(A) + trans(B) + trans(C) + trans(continuous)).strip().split('\n')))
if debug:
    print('\n'.join(map(''.join, m[:-1]))+'\n')
print('Part 2:', ord(m[-1][0]))