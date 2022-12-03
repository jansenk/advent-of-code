def iterlines(day_num, is_test=False):
    test_filename = '-test' if is_test else ''
    with open(f'advent/2022/input_files/{day_num}{test_filename}.txt') as f:
        for line in f:
            yield line.strip()