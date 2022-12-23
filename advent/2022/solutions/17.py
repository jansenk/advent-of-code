import itertools
from operator import is_
from turtle import left
from ..utils import iterlines
from advent.util.points import Direction, Point

BLANK_LINE = [False, False, False, False]
FLAT = [
    BLANK_LINE,
    BLANK_LINE,
    BLANK_LINE,
    [True, True, True, True],
]

PLUS = [
    BLANK_LINE
    [False, True, False, False],
    [True, True, True, False],
    [False, True, False, False],
]

ELL = [
    BLANK_LINE
    [False, False, True, False],
    [False, False, True, False],
    [True, True, True, False],
]

TALL = [
    [True, False, False, False],
    [True, False, False, False],
    [True, False, False, False],
    [True, False, False, False],

]

SQUARE = [
    BLANK_LINE,
    BLANK_LINE,
    [True, True],
    [True, True],
]

class Shape:
        
    def __init__(self, points, bottom, left, right):
        self.points = set(points)
        self.bottom_indices = set(bottom)
        self.left_indices = set(left)
        self.right_indices = set(right)


FLAT_POINTS = [
    Point(0, 0),
    Point(1, 0),
    Point(2, 0),
    Point(3, 0),
]

PLUS_POINTS = [
    Point(1, 0),
    Point(0, 1),
    Point(1, 1),
    Point(2, 1),
    Point(1, 2),
]

ELL_POINTS = [
    Point(0, 0),
    Point(1, 0),
    Point(2, 0),
    Point(2, 1),
    Point(2, 2),
]

TALL_POINTS = [
    Point(0, 0),
    Point(0, 1),
    Point(0, 2),
    Point(0, 3),
]

SQUARE_POINTS = [
    Point(0, 0),
    Point(1, 0),
    Point(0, 1),
    Point(1, 1),
]

# FLAT = Shape(
#     FLAT_POINTS,
#     FLAT_POINTS,
#     [FLAT_POINTS[0]],
#     [FLAT_POINTS[-1]]
# )

# PLUS = Shape(
#     PLUS_POINTS,
#     [
#         PLUS_POINTS[1],
#         PLUS_POINTS[3],
#         PLUS_POINTS[4]
#     ],
#     [
#         PLUS_POINTS[0],
#         PLUS_POINTS[1],
#         PLUS_POINTS[4]

#     ],
#     [
#         PLUS_POINTS[0],
#         PLUS_POINTS[3],
#         PLUS_POINTS[4]
#     ],
# )

# ELL = Shape(
#     ELL_POINTS,
#     ELL_POINTS[2:],
#     ELL_POINTS[:3],
#     [
#         ELL_POINTS[0],
#         ELL_POINTS[1],
#         ELL_POINTS[-1]
#     ]
# )

# TALL = Shape(
#     TALL_POINTS,
#     [TALL_POINTS[-1]],
#     TALL_POINTS,
#     TALL_POINTS
# )

# SQUARE = Shape(
#     SQUARE_POINTS,
#     SQUARE_POINTS[2:],
#     [
#         SQUARE_POINTS[0],
#         SQUARE_POINTS[2]
#     ],
#     [
#         SQUARE_POINTS[1],
#         SQUARE_POINTS[3]
#     ]
# )

FLAT = Shape(
    FLAT_POINTS,
    [0, 1, 2, 3],
    [0],
    [3]
)

PLUS = Shape(
    PLUS_POINTS,
    [1, 3, 4],
    [0, 1, 4],
    [0, 3, 4],
)

ELL = Shape(
    ELL_POINTS,
    [2, 3, 4],
    [0, 1, 2],
    [0, 1, 4],
)

TALL = Shape(
    TALL_POINTS,
    [3],
    [0, 1, 2, 3],
    [0, 1, 2, 3]
)

SQUARE = Shape(
    SQUARE_POINTS,
    [2, 3],
    [0, 2],
    [1, 3]
)


SHAPES = [
    FLAT_POINTS,
    PLUS_POINTS,
    ELL_POINTS,
    TALL_POINTS,
    SQUARE_POINTS
]

def parse_wind(is_test):
    line = next(iterlines(17, is_test))
    for char in itertools.cycle(line):
        if char == "<":
            yield Direction.LEFT
        elif char == ">":
            yield Direction.RIGHT
        else:
            raise Exception

def generate_shapes():
    return itertools.cycle(SHAPES)

def push(piece, stack, )
def part1(is_test):
    shapes = generate_shapes()
    wind = parse_wind()
    
    stack = set()
    highest_point = 0
    