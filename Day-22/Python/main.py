import sys

cmds = []
for line in sys.stdin:
    line = line.strip()
    if line != 'deal into new stack':
        cmds.append(line)
    else:
        cmds.extend(['deal with increment -1', 'cut 1'])

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def inv_mod(a, m):
    if a < 0:
        a += m
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception
    else:
        return x % m

def simulate(n_cards, cmds=cmds, find=None):
    # Old version, renewed using crunch method
    '''
    cards = list(range(n_cards))
    for line in cmds:
        if line.startswith('cut'):
            cut = int(line.split()[1])
            cards = list(map(lambda x: cards[(x + cut) % n_cards], range(n_cards)))
        else:
            increment = int(line.split()[3])
            # alternatively, since n_cards is prime, can use pow(increment, n_cards - 2, n_cards)
            cards = list(map(lambda x: cards[x * inv_mod(increment, n_cards) % n_cards], range(n_cards)))
    return cards
    '''
    if find == None:
        find = list(range(n_cards))
    cut, increment = crunch(n_cards, cmds)
    cut = int(cut.split()[1])
    increment = int(increment.split()[3])
    return list(map(lambda x: (x * inv_mod(increment, n_cards) + cut) % n_cards, find))

def crunch(n_cards, cmds):
    cmds2 = cmds.copy()
    for _ in range(len(cmds2)):
        for i in range(1, len(cmds2)):
            line, line2 = cmds2[i - 1], cmds2[i]
            if line.startswith('deal') and line2.startswith('cut'):
                increment = int(line.split()[3])
                cut = int(line2.split()[1])
                cmds2[i] = cmds2[i - 1]
                cmds2[i - 1] = f'cut {cut * inv_mod(increment, n_cards) % n_cards}'
    s, p = 0, 1
    for cmd in cmds2:
        if cmd.startswith('deal'):
            p *= int(cmd.split()[3])
            p %= n_cards
        else:
            s += int(cmd.split()[1])
            s %= n_cards
    return [f'cut {s}', f'deal with increment {p}']

def decompose(num):
    seq = []
    while num:
        if num % 2 == 0:
            num //= 2
            seq.append('mul 2')
        else:
            num -= 1
            seq.append('plus 1')
    return seq[::-1]

# for debugging, compose and decompose are inverses
def compose(seq):
    num = 0
    for c in seq:
        if c == 'plus 1':   num += 1
        else:               num *= 2
    return num

BIG, BIG2 = 119315717514047, 101741582076661
print('Part 1:', simulate(10007).index(2019))
old_cmds = crunch(BIG, cmds)
new_cmds = []
for com in decompose(BIG2):
    new_cmds = crunch(BIG, new_cmds + [new_cmds, old_cmds][com == 'plus 1'])
print('Part 2:', simulate(BIG, cmds=new_cmds, find=[2020])[0])