def iterate_while_tracking(iterable, operation, qualifier):
    """
    Returns: (best_index, best_item, best_value)
    """
    current_value = None
    best_value = None
    best_item = None
    best_index = None
    for i, item in enumerate(iterable):
        current_value = operation(item)
        if best_item is None or qualifier(current_value, best_value):
            best_value = current_value
            best_item = item
            best_index = i
    return best_index, best_item, best_value

class Qualifiers:
    @staticmethod
    def smallest(current, best):
        return current < best

    @staticmethod
    def largest(current, best):
        return current > best

def assertEqual(a, b):
    if a != b:
        s = "{} does not equal {}".format(a, b)
        raise AssertionError(s)