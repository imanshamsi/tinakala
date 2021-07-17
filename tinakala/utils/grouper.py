from itertools import zip_longest


def iterate_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in zip_longest(*args))
