import itertools
from utils import distance

def held_karp(points):
    n = len(points)
    dp = {}

    for k in range(1, n):
        dp[(1 << k, k)] = distance(points[0], points[k])

    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = sum(1 << i for i in subset)
            for j in subset:
                prev = bits & ~(1 << j)
                dp[(bits, j)] = min(
                    dp[(prev, k)] + distance(points[k], points[j])
                    for k in subset if k != j
                )

    bits = (1 << n) - 2
    return min(dp[(bits, j)] + distance(points[j], points[0]) for j in range(1, n))