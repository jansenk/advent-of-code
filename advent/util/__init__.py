def minmax(iterable):
    iterator = iter(iterable)
    first = next(iterator)
    current_min = first
    current_max = first
    for element in iterator:
        if element < current_min:
            current_min = element
        if element > current_max:
            current_max = element
    return current_min, current_max