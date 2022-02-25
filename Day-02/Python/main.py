arr = list(map(int, input().split(',')))

def intcode(arr, noun, verb):
    pos = 0
    arr[1] = noun
    arr[2] = verb
    while arr[pos] != 99:
        if arr[pos] == 1:
            arr[arr[pos + 3]] = arr[arr[pos + 1]] + arr[arr[pos + 2]]
            pos += 4
        elif arr[pos] == 2:
            arr[arr[pos + 3]] = arr[arr[pos + 1]] * arr[arr[pos + 2]]
            pos += 4
        else:
            pos += 1
    return arr[0]
print('Part 1:', intcode(arr.copy(), 12, 2))

for n in range(100):
    for v in range(100):
        if intcode(arr.copy(), n, v) == 19690720:
            print('Part 2:', 100 * n + v)