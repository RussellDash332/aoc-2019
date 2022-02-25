s, e = list(map(int, input().split('-')))

def check(n, t=0):
    c = [False, True]

    s = str(n)
    if t:
        for i in range(len(s) - 3):
            if s[i] != s[i + 1] == s[i + 2] != s[i + 3]:
                c[0] = True
                break
        c[0] |= s[0] == s[1] != s[2]
        c[0] |= s[-1] == s[-2] != s[-3]
    else:
        for i in range(len(s) - 1):
            if s[i] == s[i + 1]:
                c[0] = True
                break

    for i in range(len(s) - 1):
        if s[i] > s[i + 1]:
            c[1] = False
            break
    
    return int(all(c))

print('Part 1:', sum(map(check, range(s, e + 1))))
print('Part 2:', sum(map(lambda x: check(x, 1), range(s, e + 1))))