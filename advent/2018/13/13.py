from enum import Enum
from itertools import cycle

"""
  Another fun one! I could have done this a lot easier with just some dicts,
   but the time complexity wasn't bad and I actually enjoyed myself writing this. 
"""
f = open("in")
cart_icons = ["^", ">", "v", "<"]
carts = []
cart_map = []

class Direction(Enum):
    LEFT = -1
    STRAIGHT = 0
    RIGHT = 1

    @staticmethod
    def direction_cycle():
        return cycle([Direction.LEFT, Direction.STRAIGHT, Direction.RIGHT])

class Heading(Enum):
    SOUTH = 2
    NORTH = 0
    EAST = 1
    WEST = 3

    @staticmethod
    def get(direction):
        if direction == 4:
            direction = 0
        if direction == -1:
            direction = 3
        return Heading(direction)

    def turn(self, direction):
        #print("turning")
        #print(self, direction)
        return Heading.get(self.value + direction.value)
        #print(d)

    def move(self, x, y):
        if self == Heading.NORTH:
            return x, y-1
        if self == Heading.SOUTH:
            return x, y+1
        if self == Heading.EAST:
            return x+1, y
        if self == Heading.WEST:
            return x-1, y
        print("move fucked")

    def turn_cart(self, cart, icon):
        direction = None
        if icon in ["-", "|"]:
            direction = Direction.STRAIGHT
        if icon == "/":
            if self in [Heading.NORTH, Heading.SOUTH]:
                direction = Direction.RIGHT
            else :
                direction = Direction.LEFT
        if icon == "\\":
            if self in [Heading.NORTH, Heading.SOUTH]:
                direction = Direction.LEFT
            else :
                direction = Direction.RIGHT
        if icon == "+":
            direction = next(cart.turner)
        if direction == None:
            print("direction fucked", icon)
        return self.turn(direction)


class Cart:
    def __init__(self, x, y, icon):
        self.smashed = False
        self.x = x
        self.y = y
        self.heading = Heading(cart_icons.index(icon))
        self.turner = Direction.direction_cycle()

    def move_and_turn(self):
        newX, newY = self.heading.move(self.x, self.y)
        self.x = newX
        self.y = newY
        self.get_new_heading()

    def get_new_heading(self):
        current_icon = cart_map[self.y][self.x]
        self.heading = self.heading.turn_cart(self, current_icon)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.y < other.y:
            return True
        elif self.y > other.y:
            return False
        else:
            return self.x < other.x

current_row = 0
for line in f:
    for i, c in enumerate(line):
        if c in cart_icons:
            carts.append(Cart(i, current_row, c))
    cart_map.append(line.replace("v", "|").replace("^", "|").replace(">", "-").replace("<", "-"))
    current_row += 1

# done = False
# while not done:
#     carts.sort()
#     for cart in carts:
#         cart.move_and_turn()
#         if carts.count(cart) > 1:
#             print("collision! %d, %d" % (cart.x, cart.y))
#             done = True
#             break

done = False
while len(carts) > 1:
    carts.sort()
    for cart in carts:
        if cart.smashed:
            continue
        cart.move_and_turn()
        if carts.count(cart) > 1:
            loc = cart.x, cart.y
            print("collision! %d, %d" % (cart.x, cart.y))
            for c in carts:
                if (c.x, c.y) == loc:
                    c.smashed = True
                    c.x = -1
                    c.y = -1
    carts = [cart for cart in carts if not cart.smashed]

print("one remains!", cart.x, cart.y)
