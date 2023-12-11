from bisect import bisect_left


def bsearch(a, x):
    i = bisect_left(a, x)
    return i if i != len(a) and a[i] == x else -1
