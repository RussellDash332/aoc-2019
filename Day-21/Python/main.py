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
            try:
                arr[arr[pos + 1] + base * (c // 2)] = inp.pop()
            except:
                return ''.join(output)
            pos += 2
        elif de == 4:
            res = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)])
            try:
                output.append(chr(res))
            except:
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

def trans(txt):
    return list(map(ord, txt)) + [10]

'''
...# -> no choice but to jump
..## -> no choice but to jump
.#.# -> no choice but to jump
.### -> no choice but to jump

#..#
#.##
##.#
####
'''

# Menial labour
# (NOT A OR NOT B OR NOT C) AND D
# NOT (A AND B AND C) AND D
instruction = '''
OR B T
AND C T
AND A T
NOT T J
AND D J
WALK
'''.upper().strip()
#print(''.join(intcode(arr.copy(), trans(instruction))[:-1]))
print('Part 1:', intcode(arr.copy(), trans(instruction))[-1])

# (NOT A OR ((NOT B OR NOT C) AND H)) AND D
# (NOT A OR (NOT (B AND C) AND H)) AND D
# (NOT A OR NOT ((B AND C) OR NOT H)) AND D
# NOT (A AND ((B AND C) OR NOT H)) AND D
# NOT (A AND ((B AND C) OR NOT H)) AND D
instruction = '''
OR B T
AND C T
NOT H J
OR J T
AND A T
NOT T J
AND D J
RUN
'''.upper().strip()
#print(''.join(intcode(arr.copy(), trans(instruction))[:-1]))
print('Part 2:', intcode(arr.copy(), trans(instruction))[-1])