
with open('advent-of-code/2021/input_files/1.txt') as f:
    prev = None
    increases = 0
    for depth in f:
        depth = int(depth)
        if prev is not None and depth > prev:
            increases += 1
        prev = depth
    print(increases)

from collections import deque
with open('advent-of-code/2021/input_files/1.txt') as f:
    window = deque(
        [int(next(f)) for _ in range(3)],
        maxlen=3
    )
    prev = sum(window)
    increases = 0
    for depth in f:
        window.append(int(depth))
        window_sum = sum(window)
        if window_sum > prev:
            increases += 1
        prev = window_sum
    print(increases)