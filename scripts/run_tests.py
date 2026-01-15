import time
import csv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.nearest_neighbor import nearest_neighbor
from src.two_opt import two_opt
from src.held_karp import held_karp
from src.simulated_annealing import simulated_annealing
from utils import total_cost

def load_points(file):
    points = []
    if not os.path.exists(file):
        return []
    with open(file) as f:
        try:
            lines = f.readlines()
            if not lines: return []
            for line in lines[1:]: 
                parts = line.split()
                if len(parts) >= 2:
                    points.append((float(parts[0]), float(parts[1])))
        except ValueError:
            pass
    return points

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "../results/results.csv")
os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)

with open(RESULTS_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["N", "Algorithm", "Cost", "Time"])

    test_sizes = [10, 15, 20, 50, 100, 500] 

    for n in test_sizes:
        filename = os.path.join(os.path.dirname(__file__), f"../data/random/tsp_{n}.txt")
        points = load_points(filename)
        
        if not points:
            continue
            
        print(f"Running tests for N={n}...")

        start = time.time()
        tour_nn, cost_nn = nearest_neighbor(points)
        time_nn = time.time() - start
        writer.writerow([n, "Nearest Neighbor", cost_nn, time_nn])

        if n <= 20:
            start = time.time()
            cost_hk = held_karp(points)
            time_hk = time.time() - start
            writer.writerow([n, "Held-Karp", cost_hk, time_hk])

        start = time.time()
        tour_2opt, cost_2opt = two_opt(tour_nn, points)
        time_2opt = time.time() - start
        writer.writerow([n, "2-Opt", cost_2opt, time_nn + time_2opt])

        start = time.time()
        tour_sa, cost_sa = simulated_annealing(tour_nn, points, T=1000, alpha=0.99)
        time_sa = time.time() - start
        writer.writerow([n, "Simulated Annealing", cost_sa, time_nn + time_sa])

print("Tests finished.")