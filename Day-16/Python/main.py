sig = list(map(int, list(input())))
base = [0, 1, 0, -1]

# To visualize matrices
def get_matrix(size):
    mat = []
    for i in range(size):
        base2 = []
        base3 = []
        for b in base:
            base2.extend([b] * (i + 1))
        while len(base3) <= size + 1:
            base3.extend(base2)
        base3.pop(0)
        mat.append(base3[:size])
    for r in mat:
        print(' '.join(map(lambda x: '01!'[x], r)))

def simulate(sig, use_offset):
    offset = use_offset * int(''.join(map(str, sig[:7])))
    for _ in range(100):
        ret = []
        for i in range(len(sig)):
            base2 = []
            base3 = []
            for b in base:
                base2.extend([b] * (i + 1))
            while len(base3) <= len(sig) + 1:
                base3.extend(base2)
            base3.pop(0)
            base3 = base3[:len(sig)]
            c = 0
            for j in range(len(sig)):
                c += sig[j] * base3[j]
            ret.append(abs(c) % 10)
        sig = ret
    return ''.join(map(str, sig[offset:offset+8]))

print('Part 1:', simulate(sig.copy(), False))
# Too long
#print('Part 2:', simulate((sig*10000).copy(), True))

# Note that on each phase, the lower half submatrix forms an upper triangular that resembles a cumulative sum
# Since offset > len(sig) / 2, we can cheese this
sig *= 10000
offset = int(''.join(map(str, sig[:7])))
sig = sig[offset:]
for _ in range(100):
    ret = []
    cs = 0
    for i in sig[::-1]:
        cs += i
        ret.append(cs % 10)
    sig = ret[::-1]
print('Part 2:', ''.join(map(str, sig[:8])))