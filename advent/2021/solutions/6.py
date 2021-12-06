from collections import Counter

test_fish = [3, 4, 3, 1, 2]

def parse_fish():
    with open('advent/2021/input_files/6.txt') as f:
        return list(map(int, f.readline().split(',')))

def spawn_fish(fish):
    fish_count = Counter(fish)
    fishes = [fish_count[i] for i in range(9)]
    for day in range(1, 257):
        next_fishes = [0 for _ in range(9)]
        for i in range(8):
            next_fishes[i] = fishes[i+1]
        next_fishes[6] += fishes[0]
        next_fishes[8] = fishes[0]
        # print(f'After {day} days: {next_fishes}')
        if day in (18, 80, 256):
            print(f'After {day} days there would be a total of {sum(next_fishes)} fish')
        fishes = next_fishes        

# spawn_fish(test_fish)
spawn_fish(parse_fish())