arr = list(map(int, input().split(',')))

def extract(opcode):
    a, b, c, de = opcode % 100000 // 10000, opcode % 10000 // 1000, opcode % 1000 // 100, opcode % 100
    return a, b, c, de

def intcode(arr, inp):
    pos = 0
    while True:
        _, b, c, de = extract(arr[pos])
        if de == 99:
            return
        elif de == 1:
            arr[arr[pos + 3]] = (arr[pos + 1] if c else arr[arr[pos + 1]]) + (arr[pos + 2] if b else arr[arr[pos + 2]])
            pos += 4
        elif de == 2:
            arr[arr[pos + 3]] = (arr[pos + 1] if c else arr[arr[pos + 1]]) * (arr[pos + 2] if b else arr[arr[pos + 2]])
            pos += 4
        elif de == 3:
            arr[arr[pos + 1]] = inp
            pos += 2
        elif de == 4:
            res = (arr[pos + 1] if c else arr[arr[pos + 1]])
            if res:
                return res
            pos += 2
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

print('Part 1:', intcode(arr.copy(), 1))
print('Part 2:', intcode(arr.copy(), 5))