"""
Another tough one, and not in a fun way >.<
Lots of off-by one errors in REALLY tricky places to find

I solved part 1 with a naiive "add up the 3 by 3" solution,
 hoping that part 2 would be a softball but no!

Where would the fun be in that? ;)

One thing I love is that I added a print statement
 for every size block I'm calculating, and you can
 see the iterations get faster and faster as the
 rolling sum gets larger and larger on the grid
"""
import sys
INPUT_SERIAL = 5719
TEST_SERIAL = 18
TEST_SERIAL2 = 42


def position_value(x, y, original=False):
    # Find the fuel cell's rack ID, which is its X coordinate plus 10.
    rack_id_c = 10 if original else 11
    rack_id = x + rack_id_c
    # Begin with a power level of the rack ID times the Y coordinate.
    power_c = y if original else y + 1
    power = rack_id * power_c
    # Increase the power level by the value of the grid serial number (your puzzle input).
    power += SERIAL
    # Set the power level to itself multiplied by the rack ID.
    power *= rack_id
    # Keep only the hundreds digit of the power level
    power = int(str(power)[-3]) if power >= 100 else 0
    # Subtract 5 from the power level
    power -= 5
    return power

pos_val_tests = [
                    (3, 5, 8, 4),
                    (122, 79, 57, -5),
                    (217, 196, 39, 0),
                    (101, 153, 71, 4)
                ]

for tc in pos_val_tests:
    SERIAL = tc[2]
    val = position_value(tc[0], tc[1], original=True)
    if val != tc[3]:
        print("position value errors", tc, val)

SERIAL = INPUT_SERIAL

def print_grid_starting_at(x, y, g, s, advent_coords=False):
    t = "%d   " * s
    if advent_coords:
        x -= 1
        y -= 1
    for yv in range(s):
        for xv in range(s):
            v = position_values[x+xv][y+yv]
            if v > 0:
                sys.stdout.write(" ")
            sys.stdout.write(str(v))
            sys.stdout.write("   ")
        sys.stdout.write("\n")
        sys.stdout.flush()


position_values = [[position_value(x, y) for y in range(300)] for x in range(300)]
current_horizontal_chunks = None


def get_horizontal_chunk_value(x, y, chunk_size=None):
    if current_horizontal_chunks[x][y] is None:
        current_horizontal_chunks[x][y] = calc_horizontal_chunk_value(x, y, chunk_size)
    return current_horizontal_chunks[x][y]


def calc_horizontal_chunk_value(x, y, chunk_size):
    if x == 0:
        chunk_value = 0
        for c in range(chunk_size):
            chunk_value += position_values[x+c][y]
        return chunk_value
    else:
        return get_horizontal_chunk_value(x-1, y, chunk_size) + position_values[x+(chunk_size-1)][y] - position_values[x-1][y]


block_values = None


def get_block_value(x, y, chunk_size):
    if block_values[x][y] is None:
        block_values[x][y] = calc_block_value(x, y, chunk_size)
    return block_values[x][y]


def calc_block_value(x, y, block_size):
    if y == 0:
        block_value = 0
        for b in range(block_size):
            block_value += get_horizontal_chunk_value(x, y+b, block_size)
        return block_value
    else:
        return get_block_value(x, y-1, block_size) + get_horizontal_chunk_value(x, y+(block_size-1), block_size) - get_horizontal_chunk_value(x, y-1, block_size)

def findBest(x, y, val, best, sgs):
    if val < best[0]:
        return best
    return val, (x, y), sgs

best = (float("-inf"), (0,0), 0)

for bs in range(1, 300):
    print("Block size= %d" % bs)
    bs_adjusted = 300 - (bs -1)
    current_horizontal_chunks = [[None for y in range(300)] for x in range(bs_adjusted)]
    block_values = [[None for y in range(bs_adjusted)] for x in range(bs_adjusted)]
    for x in range(bs_adjusted):
        for y in range(bs_adjusted):
            best = findBest(x, y, calc_block_value(x, y, bs), best, bs)

print("Serial: %d" % SERIAL)
print("Highest value: %d\nPosition: (%d, %d)\nBlock size: %d" % (best[0], best[1][0]+1, best[1][1]+1, best[2]))



#print_grid_starting_at(20, 60, position_values, 5, advent_coords=True)
#print_grid_starting_at(best[1][0]-1, best[1][1]-1, position_values, best[2] + 2)
