import time

arr = list(map(int, input().split(','))) + [0] * 10000

def extract(opcode):
    a, b, c, de = opcode % 100000 // 10000, opcode % 10000 // 1000, opcode % 1000 // 100, opcode % 100
    return a, b, c, de

def intcode(arr, inp=[0]*10000, debug=False):
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
            if debug:
                print('ASKING FOR INPUT...', arr[arr[pos + 1] + base * (c // 2)])
                time.sleep(1)
            pos += 2
        elif de == 4:
            res = (arr[pos + 1] if c == 1 else arr[arr[pos + 1] + base * (c // 2)])
            if debug:
                if len(output) % 3 == 2:
                    print(f'OUTPUTING... {res} at position ({output[-2]}, {output[-1]})')
                time.sleep(0.001)
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

def draw(game):
    xmax = max(map(lambda x: x[0], game))
    ymax = max(map(lambda x: x[1], game))
    for y in range(ymax + 1):
        for x in range(xmax + 1):
            print(['.', '\033[94m+\033[0m', '#', '\033[95m=\033[0m', '\033[91mo\033[0m'][game[(x, y)]], end='')
        print()
    print()

game = {}
res = intcode([1] + arr.copy()[1:], debug=False)
pos = 0
while pos < len(res):
    game[(res[pos], res[pos + 1])] = res[pos + 2]
    pos += 3
blocks = len([x for x in game if game[x] == 2])
print('Part 1:', blocks)

def play(game, debug=False):
    step = 0
    blocks = len([x for x in game if game[x] == 2])
    moves = []
    ballx, bally = [x for x in game if game[x] == 4][0]
    padx, pady = [x for x in game if game[x] == 3][0]
    dx, dy = 1, 1
    while blocks != 0:
        step += 1
        bounce = False
        for rx, ry in [(dx, 0), (0, dy), (dx, dy)]:
            if game[((ballx + rx, bally + ry))] in [1, 2]:
                if game[((ballx + rx, bally + ry))] == 2:
                    blocks -= 1
                    game[((ballx + rx, bally + ry))] = 0
                dx -= 2*rx
                dy -= 2*ry
                bounce = True
                break
        if bounce:
            continue
        game[(ballx, bally)], game[((ballx + dx, bally + dy))] = 0, 4
        ballx += dx
        bally += dy
        if ballx == padx + dx:
            game[(padx, pady)], game[((padx + dx, pady))] = 0, 3
            padx += dx
            moves.append(dx)
        else:
            moves.append(0)
        if bally == pady - 1:
            dy = -dy
        if debug:
            draw(game)
    if debug:
        draw(game)
    return lambda: moves, step

autoplay = play(game.copy(), debug=False)
moves = [0] + autoplay[0]()
debug = False
if debug:
    # Might take a while but good visualization
    for i in range(len(moves) + 1):
        game = {}
        res = intcode([2] + arr.copy()[1:], inp=moves[:i], debug=False)
        pos = 0
        while pos < len(res):
            game[(res[pos], res[pos + 1])] = res[pos + 2]
            pos += 3
        draw(game)
else:
    game = {}
    res = intcode([2] + arr.copy()[1:], inp=moves, debug=False)
    pos = 0
    while pos < len(res):
        game[(res[pos], res[pos + 1])] = res[pos + 2]
        pos += 3
print('Part 2:', game[(-1, 0)])