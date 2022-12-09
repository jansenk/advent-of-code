def iterlines(day_num, is_test=False, test_case=None):
    test_suffix = '' if test_case is None else str(test_case)
    is_test = is_test or test_case is not None
    test_filename = f'-test{test_suffix}' if is_test else ''
    with open(f'advent/2022/input_files/{day_num}{test_filename}.txt') as f:
        for line in f:
            yield line.strip()