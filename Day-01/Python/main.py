import sys

s, t = 0, 0
for line in sys.stdin:
    line = int(line) // 3 - 2
    s += line
    while line > 0:
        t += line
        line = line // 3 - 2
print("Part 1:", s)
print("Part 2:", t)