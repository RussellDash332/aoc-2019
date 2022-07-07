from itertools import permutations
from copy import deepcopy
from collections import deque

arr = list(map(int, input().split(',')))

def extract(opcode):
    a, b, c, de = opcode % 100000 // 10000, opcode % 10000 // 1000, opcode % 1000 // 100, opcode % 100
    return a, b, c, de

def st(arr, pos):
    idx = arr[pos + 1]
    arr = list(map(str, arr))
    arr[pos] =  '\033[91m' + arr[pos] +  '\033[0m'
    arr[idx] =  '\033[92m' + arr[idx] +  '\033[0m'
    return ', '.join(arr)

def intcode(arr, inp, pos=0):
    while True:
        if debug:
            print(pos, '\t', st(arr, pos))
        _, b, c, de = extract(arr[pos])
        if de == 99:
            return None, None
        elif de == 1:
            arr[arr[pos + 3]] = (arr[pos + 1] if c else arr[arr[pos + 1]]) + (arr[pos + 2] if b else arr[arr[pos + 2]])
            pos += 4
        elif de == 2:
            arr[arr[pos + 3]] = (arr[pos + 1] if c else arr[arr[pos + 1]]) * (arr[pos + 2] if b else arr[arr[pos + 2]])
            pos += 4
        elif de == 3:
            arr[arr[pos + 1]] = inp.popleft()
            pos += 2
        elif de == 4:
            res = (arr[pos + 1] if c else arr[arr[pos + 1]])
            inp.append(res)
            return inp, pos + 2
        elif de == 5:
            if (arr[pos + 1] if c else arr[arr[pos + 1]]):
                pos = (arr[pos + 2] if b else arr[arr[pos + 2]])
            else:
                pos += 3
        elif de == 6:
            if not (arr[pos + 1] if c else arr[arr[pos + 1]]):
                pos = (arr[pos + 2] if b else arr[arr[pos + 2]])
            else:
                pos += 3
        elif de == 7:
            arr[arr[pos + 3]] = int((arr[pos + 1] if c else arr[arr[pos + 1]]) < (arr[pos + 2] if b else arr[arr[pos + 2]]))
            pos += 4
        elif de == 8:
            arr[arr[pos + 3]] = int((arr[pos + 1] if c else arr[arr[pos + 1]]) == (arr[pos + 2] if b else arr[arr[pos + 2]]))
            pos += 4
        else:
            pos += 1

def simulate():
    mts = 0
    old_arr = arr.copy()
    for ps in permutations(range(5)):
        curr_arr = old_arr.copy()
        ret = 0
        for p in ps:
            inp, _ = intcode(curr_arr, deque([p, ret]))
            ret = inp[-1]
        mts = max(mts, ret)
    return mts

def simulate2():
    amps = []
    mts = 0
    for _ in range(5):
        amps.append(arr.copy())
    for ps in permutations(range(5)):
        local_amps = deepcopy(amps)
        pos = [0, 0, 0, 0, 0]
        inps = [deque([p + 5]) for p in ps]
        inps[0].append(0)
        halt = False
        while True:
            for i in range(5):
                inp, new_pos2 = intcode(local_amps[i], inps[i], pos[i])
                if inp == new_pos2 == None:
                    halt = True
                    break
                new_pos = new_pos2
                inps[(i + 1) % 5].extend(inp)
                pos[i] = new_pos
                if i == 4:
                    mts = max(mts, inp[0])
                inps[i].clear()
            if halt:
                break
    return mts

debug = False
print('Part 1:', simulate())
print('Part 2:', simulate2())