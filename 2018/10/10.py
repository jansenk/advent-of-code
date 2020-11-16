"""
This one was a lot of fun!!
I really had no idea how to know when the letters were aligned, so I tested it a bit.
I made some assumptions that made things harder that it needed to:
1) Letters wouldn't necessarily be aligned
2) Letters might be far from one another
So I decided for each tick:
    I would calculate the distance to each position
    combine the distance of the 10 closest positions (due to assumption #2)
    and then combine all of those together somehow into a "tick value"
I messed around with the test data, and even though it was slow to calculate
the values for some 30,000 ticks, i totally got the right result.

People online did a much faster test, they tested for when the bounding box was the smallest.
I didn't even think of that because of my above assumptions but this was a neat problem
It was more of a problem-solving problem than an actual algorithmic problem
"""
import math, re, sys
# position=< 7,  0> velocity=<-1,  0>
p = re.compile('position=< *(-?\d*?), *(-?\d*?)> velocity=< *(-?\d*?), *(-?\d*?)>')
f = open("in2")


def make_function(x, y, vx, vy):
    return lambda t: (int(x) + (t * int(vx)), int(y) + (t * int(vy)))


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def euclidean_distance(p1, p2):
    return math.sqrt(math.pow(abs(p1[0] - p2[0]), 2) + math.pow(abs(p1[1] - p2[1]), 2))


def mean(l):
    if not l:
        return 0
    return sum(l) / len(l)


def median(l):
    if not l:
        return 0
    return sorted(l)[int(len(l) / 2)]


distance_functions = dict(man=manhattan_distance, euc=euclidean_distance)
combining_functions = dict(sum=sum, avg=mean, med=median)

def calc_distances(state, cf, df):
    # return [[(distance_function(p1, p2), p2) for p2 in state] for p1 in state]
    return [cf(sorted([df(p1, p2) for p2 in state])[1:10]) for p1 in state]

# don't try to parse the letters
# you won't be able to figure it out
# keep going for a while, print at
# places where the distance from
# the closest 10 positions is the least


matches = [p.match(line).groups() for line in f]
fncts = [make_function(m[0], m[1], m[2], m[3]) for m in matches]
#for d_i in distance_functions:
#    for c_i1 in combining_functions:
#        for c_i2 in combining_functions:
#            print("distance=%s combining_distances_from_a_point=%s combining_all_distance_sums=%s" % (d_i, c_i1, c_i2))
#            ds = []
#            for t in range(8):
#                state = map(lambda f: f(t), fncts)
#                distances = calc_distances(state, combining_functions[c_i1], distance_functions[d_i])
#                ds.append(combining_functions[c_i2](distances))
#            print(ds)

#man avg sum
ds = []
local_mins = []
decreasing = True
prev = 0
min_d = float('inf')
min_t = 0
#for t in range(20000, 30000):
#    state = map(lambda f: f(t), fncts)
#    distances = calc_distances(state, mean, manhattan_distance)
#    d = sum(distances)
#    if d < min_d:
#        min_d = d
#        min_t = t
#    ds.append(d)


def print_tick(t):
    state = map(lambda f: f(t), fncts)
    sbX = sorted(state, key=lambda x: x[0])
    sbY = sorted(state, key=lambda x: x[1])
    state = set(state)
    minX = sbX[0][0]
    maxX = sbX[-1][0]
    minY = sbY[0][1]
    maxY = sbY[-1][1]
    for y in range(minY, maxY+1):
        for x in range(minX, maxX+1):
            sys.stdout.write('#' if (x, y) in state else '.')
        sys.stdout.write('\n')
        sys.stdout.flush()

print_tick(10027)













