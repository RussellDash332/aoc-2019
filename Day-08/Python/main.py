w, h = 25, 6
data = input()

pic = [[[data[w*h*i + w*r + c] for c in range(w)] for r in range(h)] for i in range(len(data) // (w * h))]
def count(layer, v):
    return sum(map(lambda x: x.count(v), layer))

layer = min(pic, key=lambda x: count(x, '0'))
print('Part 1:', count(layer, '1') * count(layer, '2'))

decode = [['' for _ in range(w)] for _ in range(h)]
for r in range(h):
    for c in range(w):
        for l in range(len(pic)):
            if pic[l][r][c] != '2':
                decode[r][c] = '.#'[int(pic[l][r][c])]
                break
print('Part 2:')
print('\n'.join(map(lambda x: ''.join(x), decode)))