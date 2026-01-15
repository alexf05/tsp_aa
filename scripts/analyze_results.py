import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(__file__)
RESULTS_FILE = os.path.join(BASE_DIR, "../results/results.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "../results")

def load_results(filename):
    data = defaultdict(list)
    if not os.path.exists(filename):
        return data
        
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                n = int(row["N"])
                alg = row["Algorithm"]
                cost = float(row["Cost"])
                time_val = float(row["Time"])
                data[n].append((alg, cost, time_val))
            except ValueError:
                continue
    return data

def get_best_solutions(data):
    best_known = {}
    for n, entries in data.items():
        hk_cost = next((cost for alg, cost, _ in entries if alg == "Held-Karp"), None)
        if hk_cost:
            best_known[n] = hk_cost
        else:
            best_known[n] = min(cost for _, cost, _ in entries)
    return best_known

def plot_time(data):
    times = defaultdict(list)
    for n, entries in data.items():
        for alg, _, t in entries:
            times[alg].append((n, t))

    plt.figure(figsize=(10, 6))
    for alg, values in times.items():
        values.sort()
        x = [v[0] for v in values]
        y = [v[1] for v in values]
        plt.plot(x, y, marker="o", label=alg)

    plt.yscale("log")
    plt.xlabel("Număr noduri (N)")
    plt.ylabel("Timp execuție (s) - Log Scale")
    plt.title("Analiza Performanței Temporale")
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.savefig(os.path.join(OUTPUT_DIR, "time_vs_n.png"))

def plot_quality(data, best_known):
    quality = defaultdict(list)

    for n, entries in data.items():
        if n not in best_known: continue
        opt = best_known[n]
        
        for alg, cost, _ in entries:
            deviation = 100 * (cost - opt) / opt
            quality[alg].append((n, deviation))

    plt.figure(figsize=(10, 6))
    for alg, values in quality.items():
        values.sort()
        x = [v[0] for v in values]
        y = [v[1] for v in values]
        if alg != "Held-Karp":
            plt.plot(x, y, marker="o", label=alg)

    plt.xlabel("Număr noduri (N)")
    plt.ylabel("Deviația față de Optim/Best (%)")
    plt.title("Calitatea Soluțiilor (Gap)")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(OUTPUT_DIR, "quality_vs_n.png"))

if __name__ == "__main__":
    data = load_results(RESULTS_FILE)
    if data:
        best_known = get_best_solutions(data)
        plot_time(data)
        plot_quality(data, best_known)