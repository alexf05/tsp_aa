import random
import math
from utils import total_cost

def simulated_annealing(tour, points, T=1000, alpha=0.995):
    current = tour[:]
    best = tour[:]
    current_cost = total_cost(current, points)
    best_cost = current_cost

    while T > 1:
        i, j = sorted(random.sample(range(len(tour)), 2))
        new = current[:i] + current[i:j][::-1] + current[j:]
        new_cost = total_cost(new, points)

        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / T):
            current, current_cost = new, new_cost
            if new_cost < best_cost:
                best, best_cost = new, new_cost

        T *= alpha

    return best, best_cost