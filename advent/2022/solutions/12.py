from collections import defaultdict, namedtuple
import re
from advent.util.points import Point, cardinal_surrounding_points, Direction, move
from typing import List
from ..utils import iterlines

def _convert_point(x, y, rows):
    return Point(
        x,
        (rows - 1) - y
    )

class Map:
    height_conversion = "abcdefghijklmnopqrstuvwxyz"
    
    @staticmethod
    def load(is_test):
        return Map(list(iterlines(12, is_test)))
    
    def __init__(self, m:List[str]):
        self.start_point = None
        self.end_point = None
        self.m = {}
        self._load(m)

    def _load(self, m):
        rows = len(m)
        for y, str_row in enumerate(m):
            for x, height in enumerate(str_row):
                point = _convert_point(x, y, rows)
                height_num = None
                if height == "S":
                    assert self.start_point is None
                    self.start_point = point
                    height_num = 0
                elif height == "E":
                    assert self.end_point is None
                    self.end_point = point
                    height_num = 25
                else:
                    height_num = Map.height_conversion.index(height)
                self.m[point] = (height, height_num)
        assert self.m
        assert self.start_point
        assert self.end_point
        self.max_x = x
        self.max_y = y

    def height(self, p:Point):
        item = self[p]
        if item is None:
            return None
        return item[1]

    def __getitem__(self, p:Point):
        if p not in self:
            return None
        try:
            return self.m[p]
        except IndexError:
            return None
    
    def __contains__(self, p:Point):
        return all((
            p.x >= 0,
            p.x <= self.max_x,
            p.y >= 0,
            p.y <= self.max_y,
        ))
    
    def possible_moves(self, p:Point):
        moves = []
        current_height = self.height(p)
        # if current_height is None:
        #     breakpoint()
        for next_point in cardinal_surrounding_points(p):
            next_height = self.height(next_point)
            if next_height is not None and next_height <= current_height + 1:
                moves.append(next_point)
        return moves
    
    def possible_moves_2(self, p:Point):
        moves = []
        current_height = self.height(p)
        # if current_height is None:
        #     breakpoint()
        for next_point in cardinal_surrounding_points(p):
            next_height = self.height(next_point)
            if next_height is not None and next_height >= current_height - 1:
                moves.append(next_point)
        return moves


from queue import PriorityQueue

QueueItem = namedtuple("QueueItem", ["node", "prev"])
BacktrackItem = namedtuple("BacktrackItem", ["distance", "prev"])

def dijkstras(map, start, end_condition, next_points):
    q = PriorityQueue()
    q.put((0, QueueItem(start, Point(None, None))))
    backtrack = defaultdict(lambda: float('inf'))
    completed_nodes = set()
    breakpoint()
    while not q.empty():
        dist, v = q.get()
        # breakpoint()
        # print(f"Examining point ({v.node.x},{v.node.y}) [{map.height(v.node)}] - D{dist} from ({v.prev.x}, {v.prev.y})")
        if v.node in backtrack and backtrack[v.node].distance <= dist:
            print("\tSkipping")
            continue
        # if v.node in backtrack:
        #     breakpoint()
        backtrack[v.node] = BacktrackItem(dist, v.prev)
        if not isinstance(v.node, Point):
            breakpoint()
        if end_condition(v.node):
            return backtrack, v.node
        for next_point in next_points(v.node):
            if next_point in completed_nodes:
                continue
            # print(f"\tAdding ({next_point.x},{next_point.y}) [{map.height(next_point)}] to q")
            q.put((dist + 1, QueueItem(next_point, v.node)))
        completed_nodes.add(v.node)
    return backtrack, None
    
def print_backtrack(map, backtrack, unseen_heights = False, current_point=None):
    for y in range(map.max_y + 1):
        y = (map.max_y) - y
        row = ""
        for x in range(map.max_x + 1):
            p = Point(x, y)
            char = "."
            if p not in map:
                char = " "
            elif p in backtrack:
                char = "#"
            elif unseen_heights:
                char = map[p][0]
            if p == map.start_point:
                char = "S"
            if p == map.end_point:
                char = "E"
            if current_point is not None and current_point == p:
                char = "X"
            row += char
        print(row)


def find_shortest_path(is_test=False):
    heightmap = Map.load(is_test)
    backtracks, end = dijkstras(
        heightmap,
        heightmap.start_point,
        lambda p: p == heightmap.end_point,
        lambda p: heightmap.possible_moves(p)
    )
    # breakpoint()
    print_backtrack(heightmap, backtracks)
    print(backtracks[heightmap.end_point])
    
    
# find_shortest_path(False)

def find_best_scenic_trail(is_test=False):
    heightmap = Map.load(is_test)
    backtracks, end = dijkstras(
        heightmap,
        heightmap.end_point,
        lambda p: heightmap.height(p) == 0,
        lambda p: heightmap.possible_moves_2(p))
    print(backtracks[end])
    
find_best_scenic_trail(False)
        

