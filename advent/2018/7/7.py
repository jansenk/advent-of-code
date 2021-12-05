import re, string
t = "Step ([A-Z]) must be finished before step ([A-Z]) can begin."
f = open("in.txt")
reqs = [re.match(t, line.strip()).groups() for line in f]

class Node:
    def __init__(self, letter):
        self.letter = letter
        self.parents = set()
        self.children = set()

    def add_parent(self, parent):
        self.parents.add(parent)

    def add_child(self, child):
        self.children.add(child)

    def unused(self):
        return (not self.parents) and (not self.children)

    def __repr__(self):
        return self.letter

class Worker:
    def __init__(self, id):
        self.id = id
        self.node = None
        self.seconds = 0

    def tick(self):
        if not self.node:
            return None
        self.seconds -= 1
        if self.seconds == 0:
            n = self.node
            self.node = None
            return n

    def assign_node(self, node):
        self.node = node
        self.seconds = 60 + string.ascii_uppercase.find(node.letter) + 1

    def __repr__(self):
        if self.node:
            return "%d [%s] %d" % (self.id, self.node.letter, self.seconds)
        return "%d [None]" % self.id


nodes = {l: Node(l) for l in string.ascii_uppercase}
def loadNodes():
    for req in reqs:
        step1 = nodes[req[0]]
        step2 = nodes[req[1]]
        step1.add_child(step2)
        step2.add_parent(step1)


def remove_parent_from_children(l_node, stk):
    for c_node in l_node.children:
        c_node.parents.remove(l_node)
        if not c_node.parents:
            stk.append(c_node)


loadNodes()
result = ""
s = [node for node in nodes.values() if not node.parents]
while s:
    l_node = s.pop(0)
    result += str(l_node)
    remove_parent_from_children(l_node, s)
    s.sort()

print(result)
print(len(result))

loadNodes()
workers = [Worker(i) for i in range(5)]
s = [node for node in nodes.values() if not node.parents]
time = 0
result = ""
while len(result) < 26:
    print("%d seconds have passed" % time)
    print(result)
    print(s)
    for worker in workers:
        print(worker)
        if s and not worker.node:
            worker.assign_node(s.pop(0))
    for worker in workers:
        done_node = worker.tick()
        if done_node:
            remove_parent_from_children(done_node, s)
            result += str(done_node)
    s.sort()
    time += 1
print(time)
