from collections import deque

arr = list(map(int, input().split(','))) + [0] * 10000

def extract(opcode):
    a, b, c, de = opcode % 100000 // 10000, opcode % 10000 // 1000, opcode % 1000 // 100, opcode % 100
    return a, b, c, de

def intcode(arr, pos=0, inp=[]):
    base = 0
    output = []
    while True:
        a, b, c, de = extract(arr[pos])
        if de == 99:
            return arr, pos, output
        elif de == 1:
            arr[arr[pos + 3] + base * (a // 2)] = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]) + (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)])
            pos += 4
        elif de == 2:
            arr[arr[pos + 3] + base * (a // 2)] = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)]) * (arr[pos + 2] if b == 1 else arr[arr[pos + 2] + base * (b // 2)])
            pos += 4
        elif de == 3:
            if not inp:
                return arr, pos, output
            arr[arr[pos + 1] + base * (c // 2)] = inp.pop(0)
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

computer = [[arr.copy(), 0] for _ in range(50)]
waiting = [[i, -1] for i in range(50)]
q = deque(range(50))
p1, p2 = False, False
natx, naty = None, None
natys = set()
while q:
    idx = q.popleft()
    arr, pos, output = intcode(*computer[idx], inp=waiting[idx])
    computer[idx] = [arr, pos]
    q.append(idx)
    assert len(output) % 3 == 0
    for i in range(len(output) // 3):
        try:
            waiting[output[3*i]].extend(output[3*i+1:3*(i+1)])
        except:
            if not p1:
                print('Part 1:', output[3*i+2])
                p1 = True
            natx, naty = output[3*i+1:3*(i+1)]
    if not p2 and not any(waiting):
        q.append(0)
        waiting[0].extend([natx, naty])
        if naty in natys:
            print('Part 2:', naty)
            p2 = True
            q.clear()
        natys.add(naty)