from utils import distance, total_cost

def nearest_neighbor(points):
    n = len(points)
    visited = [False] * n
    tour = [0]
    visited[0] = True

    for _ in range(n - 1):
        last = tour[-1]
        next_city = min(
            (i for i in range(n) if not visited[i]),
            key=lambda i: distance(points[last], points[i])
        )
        tour.append(next_city)
        visited[next_city] = True

    return tour, total_cost(tour, points)