from ..utils.points import Point, reflect

class Sheet:
    def __init__(self):
        self.points = set()
        # self.min_x = None
        # self.max_x = None
        # # self.min_y = None
        # self.max_y = None

    def add(self, point):
        self.points.add(point)
        # self._update_minmax(point)

    # def _update_minmax(self, point):
        if all(
            # self.min_x is None,
            # self.min_y is None,
            self.max_x is None,
            self.max_y is None
        ):
            # self.min_x = point
            # self.min_y = point
            self.max_x = point
            self.max_y = point
            return

        # if point.x < self.min_x.x:
        #     self.min_x = point
        if point.x > self.max_x.x:
            self.max_x = point
        
        # if point.y < self.min_y.y:
        #     self.min_y = point
        if point.y > self.max_y.y:
            self.max_y = point
    
    def find_maxes(self):
        max_x, max_y = -1, -1
        for point in self.points:
            if point.x > max_x:
                max_x = point.x
            if point.y > max_y:
                max_y = point.y
        return max_x, max_y

    def print_sheet(self):
        max_x, max_y = self.find_maxes()
        for y in range(max_y + 1):
            line = []
            for x in range(max_x + 1):
                if Point(x, y) in self.points:
                    line.append('#')
                else:
                    line.append('.')
            print("".join(line))
    
    def _points_to_be_folded(self, predicate):
            return {point for point in self.points if predicate(point)}
    
    def _fold(self, fold_axis, fold_value):
        points_to_fold = self._points_to_be_folded(lambda p: getattr(p, fold_axis) > fold_value)
        self.points.difference_update(set(points_to_fold))
        folded_points = []
        for point in points_to_fold:
            folded_points.append(reflect(point, **{fold_axis: fold_value}))
        self.points.update(folded_points)

    def horizontal_fold(self, y):
        self._fold('y', y)

    def vertical_fold(self, x):
        self._fold('x', x)

    def fold(self, fold):
        direction, value = fold
        if direction == 'y':
            self.horizontal_fold(value)
        else:
            self.vertical_fold(value)    
 
def parse_sheet(test):
    sheet = Sheet()
    folds = []
    test_str = f'-test' if test else ''
    with open(f'advent/2021/input_files/13{test_str}.txt') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            elif line.startswith('fold'):
                fold = line.split()[2]
                direction, value = fold.split('=')
                value = int(value)
                folds.append((direction, value))
            else:
                x, y = line.split(',')
                x, y = int(x), int(y)
                p = Point(x, y)
                sheet.points.add(p)
    return sheet, folds    


def part1(test):
    sheet, folds = parse_sheet(test)
    sheet.fold(folds[0])
    print(len(sheet.points))

def part2(test):
    sheet, folds = parse_sheet(test)
    for fold in folds:
        sheet.fold(fold)
    sheet.print_sheet()

if __name__ == "__main__":
    # part1(True)
    # part1(False)
    
    part2(True)
    part2(False)