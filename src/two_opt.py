from utils import total_cost

def two_opt(tour, points):
    improved = True
    best_cost = total_cost(tour, points)

    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1:
                    continue
                new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                new_cost = total_cost(new_tour, points)
                if new_cost < best_cost:
                    tour = new_tour
                    best_cost = new_cost
                    improved = True
    
    return tour, best_cost