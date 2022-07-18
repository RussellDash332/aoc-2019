import re
from collections import defaultdict
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
            except:
                return ''.join(output)
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

def trans(txt):
    return list(map(ord, txt)) + [10]

debug = False
manual = False
if manual:
    # Let's just explore manually like it's an actual game :)
    commands = '''
    east
    east
    take semiconductor
    north
    take planetoid
    west
    take food ration
    west
    west
    take monolith
    east
    east
    north
    take space law space brochure
    north
    north
    take weather machine
    south
    south
    east
    take jam
    west
    south
    east
    north
    take antenna
    south
    south
    east
    south
    south
    east
    east
    '''.replace('\t', '').replace('    ', '')
    items = ['food ration', 'weather machine', 'antenna', 'space law space brochure', 'jam', 'semiconductor', 'planetoid', 'monolith']
else:
    # The actual code
    opp = {
        'north': 'south',
        'south': 'north',
        'west': 'east',
        'east': 'west',
        'start': ''
    }

    all_items = defaultdict(lambda: set())
    path = []
    def find_items(commands=['start'], exclude=['infinite loop', 'giant electromagnet']):
        m = intcode(arr.copy(), trans('\n'.join(commands[1:] + list(all_items[tuple(commands[1:])]))))
        if 'Alert!' in m:
            path.append(commands[1:-1])
            return
        m = m.split('\n')
        start = -m[::-1].index('Doors here lead:')-1
        try:
            end = m[start:].index('Items here:')
            end2 = m[start+end:].index('Command?')
            items = list(map(lambda x: x.strip('- '), m[start+end+1:start+end+end2-1]))
            for item in items:
                if item not in exclude:
                    check = intcode(arr.copy(), trans('\n'.join(commands[1:]+[f'take {item}']))).strip('\n\n').split('\n')
                    if check[-1] == 'Command?':
                        all_items[tuple(commands[1:])].add(f'take {item}')
        except:
            end = m[start:].index('Command?')
        dirs = list(map(lambda x: x.strip('- '), m[start+1:start+end-1]))
        for d in dirs:
            if d != opp[commands[-1]]:
                find_items(commands + [d], exclude)
    find_items()

    final_path = []
    for p in all_items:
        if all_items[p]:
            final_path.extend(p)
            final_path.extend(all_items[p])
            final_path.extend(map(opp.get, p[::-1]))
    final_path += path[0]
    if debug:
        print(intcode(arr.copy(), trans('\n'.join(final_path + ['inv']))))
    items = []
    for take_cmd in all_items.values():
        items.extend(map(lambda x: x[5:], take_cmd))
    commands = '\n'.join(final_path)

# Try all possibilities on what to drop and keep
for i in range(2**len(items)):
    take = list(map(int, bin(i)[2:].zfill(len(items))))
    drop = ['drop ' + item for i, item in enumerate(items) if not take[i]]
    m = list(map(list, intcode(arr.copy(), trans('\n'.join(commands.strip().split('\n') + drop + ['east', 'inv']))).strip().split('\n')))
    check = re.findall('\d+', ''.join(m[-1]))
    if debug:
        print('\n'.join(map(''.join, m+[[]])))
        print(', '.join(drop))
        print()
    if check:
        print('Part 1:', check[0])
        print('Part 2: THE END!')
        break