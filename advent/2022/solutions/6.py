test_inputs = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]

test_part_1_answers = [7, 5, 6, 10, 11]
test_part_2_answers = [19, 23, 23, 29, 26]
from collections import deque

def find_unique_index(s, window_size):
    buf = deque(s[:window_size-1])
    for i in range(window_size-1, len(s)):
        buf.append(s[i])
        if len(set(buf)) == window_size:
            return i + 1
        buf.popleft()
    return None

def part1(s):
    return find_unique_index(s, 4)

def part2(s):
    return find_unique_index(s, 14)

def tests():
    for part, name, answers in [(part1, "1", test_part_1_answers), (part2, "2", test_part_2_answers)]:
        print("testing part " + name)
        for s, r in zip(test_inputs, answers):
            print(f"{s}====={r}")
            assert part(s) == r 
    
with open("advent/2022/input_files/6.txt") as f:
    day6in = f.readline().strip()

tests()
print(part1(day6in))
print(part2(day6in))