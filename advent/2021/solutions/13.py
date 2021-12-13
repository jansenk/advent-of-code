from ..utils.points import Point, reflect

    
def find_maxes(points):
    max_x, max_y = -1, -1
    for point in points:
        if point.x > max_x:
            max_x = point.x
        if point.y > max_y:
            max_y = point.y
    return max_x, max_y

def print_sheet(points):
    max_x, max_y = find_maxes(points)
    for y in range(max_y + 1):
        line = []
        for x in range(max_x + 1):
            if Point(x, y) in points:
                line.append('#')
            else:
                line.append('.')
        print("".join(line))

def fold_sheet(points, fold):
    fold_axis, fold_value = fold
    points_to_fold = {point for point in points if getattr(point, fold_axis) > fold_value}
    new_points = points - set(points_to_fold)
    for point in points_to_fold:
        new_points.add(reflect(point, **{fold_axis: fold_value}))
    return new_points

def parse_sheet(test):
    sheet = set()
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
                sheet.add(p)
    return sheet, folds    


def part1(test):
    sheet, folds = parse_sheet(test)
    new_sheet = fold_sheet(sheet, folds[0])
    print(len(new_sheet))

def part2(test):
    sheet, folds = parse_sheet(test)
    for fold in folds:
        sheet = fold_sheet(sheet, fold)
    print_sheet(sheet)

if __name__ == "__main__":
    part1(True)
    part1(False)
    
    part2(True)
    part2(False)