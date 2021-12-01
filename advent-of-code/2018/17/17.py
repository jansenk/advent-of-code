import re
t = re.compile("(x|y)=(\d*), (x|y)=(\d*)\.\.(\d*)$")

inputs = [{g[0]: [int(g[1])], g[2]: range(int(g[3]), int(g[4]) + 1)} for g in [t.match(line).groups() for line in open("17int")]]
#print(inputs)
walls = set()
miny = float('inf')
maxy = float('-inf')
for vein in inputs:
    xs = []
    ys = []
    for xy in vein:
        if xy == "x":
            xs = vein[xy]
        else:
            ys = vein[xy]
    for x in xs:
        for y in ys:
            walls.add((x, y))
    miny = min(miny, ys[0])
    maxy = max(maxy, ys[-1])

print(miny, maxy)
for y in range(miny - 1, maxy + 3):
    row = ""
    for x in range(494, 508):
        row += "#" if (x, y) in walls else "."
    print(row)

source = (500, miny-1)
sources = [(source)]

class ArrayIndexEdge:

    def __init__(self, i, v):
        self.i = i
        self.j = i+1
        l = self.get_lesser(v)
        if l is None:
            l = float("-inf")
        g = self.get_greater(v)
        if g is None:
            g = float("inf")

        self.d = d

    def _get(self, x, v):
        if (x >= len(v)) or (x < 0):
            return None
        else:
            return v[x]

    def get_lesser(self, v):
        return self._get(self.i, v)

    def get_greater(self, v):
        return self._get(self.j, v)

    def __lt__(self, x):

    def __gt__(self, x):


    def __contains__(self, x, x):
        return (l <= x) and (x <= g)






    def getScope


def search_gt(l, v, min_i=0, max_i=None):
    if max_i is None:
        max_i = len(l)-1
    if min_i == max_i:
        t_i = min_i
        if l[t_i] > v:
            return l[t_i]
        else: #less than or equal to
            return l[t_i + 1]

    else:
        t_i = int((min_i + max_i) / 2)
        if l[t_i] > v:
            #to the left
            return search_gt(l, v, min_i=min_i, max_i=t_i-1)
        else:
            return search_gt(l, v, min_i = t_i+1, max_i = max_i)
            #to the right

a = [10]
b = [1, 200, 201, 300, 350, 375, 400, 200000, 3000000]
c = [200, 201, 300, 350, 375, 400, 200000, 3000000]

tests = (a, )



# class WaterLine:
#     def __init__(self, posn):
#
#
#
#
# while sources:
#     for source in sources:
#         spread_and_s
