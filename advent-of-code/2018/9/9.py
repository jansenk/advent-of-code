# I actually learned a good lesson here
# I originally represented state with a python list because I assumed python built-in pop() and insert()
# functions were good enough. They aren't!!

INPUT_STRING = "412 players; last marble is worth 71646 points"
TEST_INPUTS = [("10 players; last marble is worth 1618 points", 8317),
               ("13 players; last marble is worth 7999 points", 146373),
               ("17 players; last marble is worth 1104 points", 2764),
               ("21 players; last marble is worth 6111 points", 54718),
               ("30 players; last marble is worth 5807 points", 37305)]
EXAMPLE = ["9 players; last marble is worth 25 points", 32]


def parse_input_string(input_string):
    s = input_string.split(" ")
    return int(s[0]), int(s[6])


class MarbleGame:
    def __init__(self, p, m):
        self.p = p
        self.m = m
        self.scores = {pi: 0 for pi in range(p + 1)}
        self.current_player = 1
        self.next_marble = 1
        self.zero_node = Node(0, None, None)
        self.current_node = self.zero_node

    def next_player(self):
        self.current_player += 1
        if self.current_player > self.p:
            self.current_player = 1

    def score(self):
        #print("scoring", self.next_marble)
        #print("self.next_marble", self.next_marble)
        self.scores[self.current_player] += self.next_marble
        n = self.current_node.rotate(-7)
        self.scores[self.current_player] += n.v
        self.current_node = n.remove_me()

    def play(self):
        while self.next_marble < self.m:
            #print("tick")
            #self.zero_node.print_m()
            #print("current node", self.current_node)
            if self.next_marble % 23 == 0:
                self.score()
            else:

                self.current_node = self.current_node.rotate(1).insert_after(self.next_marble)
            self.next_player()
            self.next_marble += 1
            #print("turn over")
            #print("state", self.state)
            #print("cmi", self.current_marble_index)
            #print("nmi", self.next_marble_index)

    def top_score(self):
        return sorted(self.scores.items(), key= lambda i: i[1])[-1]

class Node:
    def __init__(self, v, prev, next):
        self.v = v
        self.prev = prev if prev is not None else self
        self.next = next if next is not None else self

    def insert_after(self, nv):
        #print("inserting %d between %d and %d" % (nv, self.v, self.next.v))
        new = Node(nv, self, self.next)
        oldnext = self.next
        self.next.prev = new
        self.next = new
        ##print("After insert: ")
        #print("me", self)
        #print("new", new)
        #print("oldnext", oldnext)
        return new

    def remove_me(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        return self.next

    def rotate(self, steps):
        if steps == 0:
            return self
        if steps < 0:
            return self.prev.rotate(steps + 1)
        return self.next.rotate(steps - 1)

    def print_m(self):
        result = [self.v]
        n = self.next
        while n != self:
            result.append(n.v)
            n = n.next
        print(result)

    def __repr__(self):
        return "(%d -> %d -> %d)" % (self.prev.v, self.v, self.next.v)



pi = parse_input_string(EXAMPLE[0])
mg = MarbleGame(pi[0], pi[1])
mg.play()
print(mg.top_score(), EXAMPLE[1])

for test_input, expected_out in TEST_INPUTS:
    pi = parse_input_string(test_input)
    mg = MarbleGame(pi[0], pi[1])
    mg.play()
    print(mg.top_score(), expected_out)

pi = parse_input_string(INPUT_STRING)
mg = MarbleGame(pi[0], pi[1])
mg.play()
print(mg.top_score())

pi = parse_input_string(INPUT_STRING)
mg = MarbleGame(pi[0], pi[1] * 100)
print("max", pi[1] * 100)
mg.play()
print(mg.top_score())