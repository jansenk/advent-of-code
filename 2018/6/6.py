

f = open("in.txt")
coords = [[int(l) for l in line.strip().split(", ")] for line in f]
sbX = sorted(coords, key=lambda x: x[0])
sbY = sorted(coords, key=lambda x: x[1])
minX = sbX[0][0]
maxX = sbX[-1][0]
minY = sbY[0][1]
maxY = sbY[-1][1]
node = "N"
area = "A"

#Try a router-style shortest path algo

def calc_d(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


#This is wrong! only send out in cardianl directions!!!
class PuzzleGrid:
    def __init__(self, aX, zX, aY, zY):
        self.posns = []
        self.counter = 1
        self.aX = aX
        self.zX = zX
        self.w = zX - aX
        self.aY = aY
        self.zY = zY
        self.h = zY - aY
        print("w=%d h=%d" % (self.w, self.h))
        self.grid = [[(area, float("inf")) for x in range(self.w + 1)] for y in range(self.h +1)]

    def adjust(self, coord):
        return coord[0] - self.aX, coord[1] - self.aY

    def get_space(self, coord):
        return self.grid[coord[1]][coord[0]]

    def set_space(self, coord, val):
        self.grid[coord[1]][coord[0]] = val

    def is_in_grid(self, coord):
        return (coord[0] >= 0) and (coord[1] >= 0) and (coord[0] <= self.w) and (coord[1] <= self.h)

    def get_coords_step_away(self, posn, d):
        n = (posn[0], posn[1] - 1)
        s = (posn[0], posn[1] + 1)
        e = (posn[0] - 1, posn[1])
        w = (posn[0] + 1, posn[1])
        return map(lambda posn2: (d, posn2), filter(lambda posn: self.is_in_grid(posn), [n, s, e, w]))

    def add_and_spread(self, coord):
        adjusted = self.adjust(coord)
        self.set_space(adjusted, (node, self.counter))
        self.posns.append((self.counter, adjusted))
        self.counter += 1

    def calculate_distances(self):
        result = dict()
        for x in range(self.w + 1):
            for y in range(self.h +1):
                current_coord = (x, y)
                distances = [(calc_d(current_coord, posn), id) for (id, posn) in self.posns]
                distances.sort(key=lambda d: d[0])
                owner = distances[0][1]
                if owner not in result:
                    result[owner] = 0
                if self.is_edge(current_coord):
                    result[owner] = float('inf')
                else:
                    result[owner] += 1
        return result

    def is_edge(self, posn):
        return (posn[0] == 0) or (posn[1] == 0) or (posn[0] == self.w) or (posn[1] == self.h)

    def get_area_owner(self, space):
        if space[0] == area:
            return space[2]
        else:
            return space[1]

    def count_safe_size(self, safe_distance):
        safe_spaces = 0
        for x in range(self.w + 1):
            for y in range(self.h + 1):
                current_coord = (x, y)
                distances = [calc_d(current_coord, posn) for (_, posn) in self.posns]
                if sum(distances) < safe_distance:
                    safe_spaces += 1
        return safe_spaces


pg = PuzzleGrid(minX, maxX, minY, maxY)
for coord in coords:
    pg.add_and_spread(coord)

m = pg.calculate_distances()
print(m)

m = filter(lambda d: d[1] != float('inf'), m.items())
m = sorted(m, key=lambda d: d[1])
print(m)


m = pg.count_safe_size(10000)
print(m)


