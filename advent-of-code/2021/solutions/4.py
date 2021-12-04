def parse_input(filename):
    with open('advent-of-code/2021/input_files/' + filename) as f:
        lines = f.readlines()
    
    numbers = lines[0].strip().split(',')
    board_index = 2
    boards = []
    while board_index < len(lines):
        board = read_board(lines[board_index:board_index+5])
        boards.append(board)
        board_index += 6

    return numbers, boards

def stripsplit(s):
    return [element for element in s.strip().split(' ') if element]

def read_board(board_lines):
    board = []
    for line in board_lines:
        board.append(stripsplit(line))
    return board

def check_horizontal(board):
    # breakpoint()
    return any((all(line) for line in board))

def check_verticals(board):
    # breakpoint()
    n = len(board[0])
    return any(all([row[column_i] for row in board]) for column_i in range(n))
            
def check_diagonals(board):
    # breakpoint()
    n = len(board[0])
    diagonals_1 = [(i, i) for i in range(n)]
    diagonals_2 = [((n-1)-i, i) for i in range(n)]
    return all(board[row][column] for column, row in diagonals_1) or all(board[row][column] for column, row in diagonals_2)

def check_board(board):
    horiz = check_horizontal(board)
    vert = check_verticals(board)
    # diag = check_diagonals(board)
    return horiz or vert

def apply_number(number, board):
    n = len(board[0])
    for row in range(n):
        for column in range(n):
            if board[row][column] == number:
                return row, column
    return -1, -1


def sum_uncovered(board, bool_board):
    n = len(board[0])
    uncovered = []
    for row in range(n):
        for column in range(n):
            if not bool_board[row][column]:
                uncovered.append(board[row][column])
    uncovered = list(map(int, uncovered))
    result = sum(uncovered)
    return result

def score_board(board, bool_board, number):
    uncovered_sum = sum_uncovered(board, bool_board)
    print(f'uncovered sum={uncovered_sum} last_number={number}')
    print(uncovered_sum * int(number))


def print_board(i, board, bool_board):
    print(f'Board {i+1}------------')
    n = len(board[0])
    row_str = "{:5} " * n
    for row in range(n):
        print_row = []
        for column in range(n):
            val = board[row][column]
            if bool_board[row][column]:
                print_row.append(f'({val})')
            else:
                print_row.append(val)
        print(row_str.format(*print_row))
    print('\n\n\n')

def part_1(numbers, boards):
    bool_boards = [[[False for _ in range(len(boards[0][0]))] for __ in range(len(boards[0]))] for ___ in range(len(boards))]
    for number in numbers:
        print(f"~~~~~ {number} ~~~~~~~~~~~~~~~~~~~~~~")
        for i, board in enumerate(boards):
            row, column = apply_number(number, board)
            if row == -1:
                continue
            bool_boards[i][row][column] = True
            if check_board(bool_boards[i]):
                score_board(board, bool_boards[i], number)
                return
            print_board(i, board, bool_boards[i])
            
def part_2(numbers, boards):
    bool_boards = [[[False for _ in range(len(boards[0][0]))] for __ in range(len(boards[0]))] for ___ in range(len(boards))]
    remaining_boards = set(range(len(boards)))
    called_numbers = []
    for number in numbers:
        print(f"~~~~~ {number} ~~~~~~~~~~~~~~~~~~~~~~ {len(remaining_boards)} remaining")
        called_numbers.append(number)
        for i in range(len(boards)):
            if i not in remaining_boards:
                continue
            
            row, column = apply_number(number, boards[i])
            if row == -1:
                continue

            bool_boards[i][row][column] = True

            if check_board(bool_boards[i]):
                print(f'Board {i+1} has won.')
                # print_board(i, boards[i], bool_boards[i])
                if len(remaining_boards) == 1:
                    print('This was the last remaining board.')
                    score_board(boards[i], bool_boards[i], number)
                    return
                else:
                    remaining_boards.remove(i)
                    print(f'Still {len(remaining_boards)} boards to go')


test_numbers, test_boards = parse_input('4-test.txt')
# part_1(test_numbers, test_boards)
# part_2(test_numbers, test_boards)

numbers, boards = parse_input('4.txt')
part_1(numbers, boards)
part_2(numbers, boards)

