f = open("in.txt")
fstr = f.readline()
#fstr = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
inputs = [int(i) for i in fstr.split(" ")]


class Node:
    def __init__(self, num_children, num_metadata):
        self.nc = num_children
        self.nm = num_metadata
        self.c = []
        self.m = []
        self.val = None

    def add_child(self, node):
        self.c.append(node)

    def add_meta(self, meta):
        self.m.append(meta)

    def sum_meta(self):
        return sum(self.m) + sum(map(lambda c: c.sum_meta(), self.c))

    def value(self):
        if self.val is None:
            self.val = self.calc_value()
        return self.val

    def calc_value(self):
        if not self.c:
            return sum(self.m)
        else:
            result = 0
            for meta in self.m:
                if meta > len(self.c):
                    continue
                mi = meta - 1
                result += self.c[mi].value()
            return result

def make_node(head):
    node = Node(inputs[head], inputs[head+1])
    head += 2
    for _ in range(node.nc):
        r = make_node(head)
        node.add_child(r[0])
        head = r[1]
    for _ in range(node.nm):
        node.add_meta(inputs[head])
        head += 1
    return node, head


n, h = make_node(0)
print(n.sum_meta())
print(n.value())



