import math

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def total_cost(tour, points):
    cost = 0
    for i in range(len(tour)):
        cost += distance(points[tour[i]], points[tour[(i + 1) % len(tour)]])
    return cost