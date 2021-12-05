import re
t = '#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)'


class Claim:
    def __init__(self, line):
        line_groupdict = re.match(t, line).groupdict()
        self.id = int(line_groupdict["id"])
        self.x = int(line_groupdict["x"])
        self.y = int(line_groupdict["y"])
        self.w = int(line_groupdict["w"])
        self.h = int(line_groupdict["h"])

    def xw(self):
        return self.x + self.w

    def yh(self):
        return self.y + self.h


claims = [Claim(l) for l in open("in.txt", "r")]
claim_map = dict()
for claim in claims:
    for x in range(claim.x, claim.xw()):
        for y in range(claim.y, claim.yh()):
            location = (x, y)
            prev_count = 0
            if location in claim_map:
                prev_count = claim_map[location]
            claim_map[location] = prev_count + 1

result = 0
for times_claimed in claim_map.itervalues():
    if times_claimed > 1:
        result = result + 1

print("There are %d inches claimed multiple times" % result)

#Definitely a suboptimal solution but it's straightforward and it works

def test_claim(claim):
    for x in range(claim.x, claim.xw()):
        for y in range(claim.y, claim.yh()):
            location = (x, y)
            if claim_map[location] > 1:
                return False
    return True


for claim in claims:
    if test_claim(claim):
        print("Claim %d does not overlap with any others" % claim.id)