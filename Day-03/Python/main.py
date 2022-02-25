w1 = list(map(lambda x: [x[0], int(x[1:])], input().split(',')))
w2 = list(map(lambda x: [x[0], int(x[1:])], input().split(',')))

int1, int2 = {}, {}

for w, i in [[w1, int1], [w2, int2]]:
    posx, posy, s = 0, 0, 0
    for dir, inc in w:
        if dir == 'R':
            for _ in range(inc):
                s += 1
                posx += 1
                if (posx, posy) not in i:
                    i[(posx, posy)] = s
        elif dir == 'U':
            for _ in range(inc):
                s += 1
                posy += 1
                if (posx, posy) not in i:
                    i[(posx, posy)] = s
        elif dir == 'D':
            for _ in range(inc):
                s += 1
                posy -= 1
                if (posx, posy) not in i:
                    i[(posx, posy)] = s
        else:
            for _ in range(inc):
                s += 1
                posx -= 1
                if (posx, posy) not in i:
                    i[(posx, posy)] = s

print('Part 1:', min(map(lambda x: abs(x[0]) + abs(x[1]), int1.keys() & int2.keys())))
print('Part 2:', min(map(lambda x: int1[x] + int2[x], int1.keys() & int2.keys())))