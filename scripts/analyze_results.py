import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import os
import numpy as np

# Setări căi fișiere
BASE_DIR = os.path.dirname(__file__)
RESULTS_FILE = os.path.join(BASE_DIR, "../results/results.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "../results")

def load_results(filename):
    data = defaultdict(list)
    if not os.path.exists(filename):
        print(f"Eroare: Fișierul {filename} nu există!")
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
    """Obține cel mai bun cost cunoscut (Held-Karp sau minimul găsit)."""
    best_known = {}
    for n, entries in data.items():
        hk_cost = next((cost for alg, cost, _ in entries if alg == "Held-Karp"), None)
        if hk_cost:
            best_known[n] = hk_cost
        else:
            best_known[n] = min(cost for _, cost, _ in entries)
    return best_known

# --- GENERARE GRAFICE ---

def plot_time(data):
    """Grafic 1: Timp de execuție vs N (Log Scale)"""
    times = defaultdict(list)
    for n, entries in data.items():
        for alg, _, t in entries:
            times[alg].append((n, t))

    plt.figure(figsize=(10, 6))
    for alg, values in times.items():
        values.sort()
        x = [v[0] for v in values]
        y = [v[1] for v in values]
        plt.plot(x, y, marker="o", label=alg, linewidth=2)

    plt.yscale("log")
    plt.xlabel("Număr Orașe (N)", fontsize=12)
    plt.ylabel("Timp (secunde) - Scară Logaritmică", fontsize=12)
    plt.title("Comparatie Timp de Execuție", fontsize=14)
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.4)
    plt.savefig(os.path.join(OUTPUT_DIR, "grafic_1_timp.png"))
    print("-> Generat grafic_1_timp.png")
    plt.close()

def plot_quality_gap(data, best_known):
    """Grafic 2: Deviația procentuală față de optim (Gap)"""
    quality = defaultdict(list)
    for n, entries in data.items():
        if n not in best_known: continue
        opt = best_known[n]
        for alg, cost, _ in entries:
            deviation = 100 * (cost - opt) / opt
            quality[alg].append((n, deviation))

    plt.figure(figsize=(10, 6))
    for alg, values in quality.items():
        if alg == "Held-Karp": continue # Gap 0, nu e relevant grafic
        values.sort()
        x = [v[0] for v in values]
        y = [v[1] for v in values]
        plt.plot(x, y, marker="s", label=alg, linewidth=2)

    plt.xlabel("Număr Orașe (N)", fontsize=12)
    plt.ylabel("Deviație față de Best (%)", fontsize=12)
    plt.title("Calitatea Soluțiilor (Eroare Relativă)", fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.savefig(os.path.join(OUTPUT_DIR, "grafic_2_calitate.png"))
    print("-> Generat grafic_2_calitate.png")
    plt.close()

def plot_bar_comparison(data, target_n=50):
    """Grafic 3: Bar Chart comparativ pentru un N specific (ex: 50 sau 100)"""
    if target_n not in data:
        # Caută cel mai mare N disponibil dacă target_n nu există
        available_ns = sorted(data.keys())
        if not available_ns: return
        target_n = available_ns[-1]

    entries = data[target_n]
    algs = [e[0] for e in entries if e[0] != "Held-Karp"]
    costs = [e[1] for e in entries if e[0] != "Held-Karp"]
    
    # Normalizare costuri pentru vizualizare mai bună (cel mai mic = 1.0)
    min_cost = min(costs) if costs else 1
    normalized_costs = [c / min_cost for c in costs]

    plt.figure(figsize=(8, 6))
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    bars = plt.bar(algs, costs, color=colors[:len(algs)], edgecolor='black')
    
    plt.ylabel("Cost Total Drum", fontsize=12)
    plt.title(f"Comparație Costuri pentru N={target_n}", fontsize=14)
    plt.grid(axis='y', alpha=0.3)
    
    # Adaugă valorile pe bare
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 1), va='bottom', ha='center', fontweight='bold')

    plt.savefig(os.path.join(OUTPUT_DIR, "grafic_3_bar_chart.png"))
    print("-> Generat grafic_3_bar_chart.png")
    plt.close()

# --- GENERARE TABELE (CSV) ---

def save_table_detailed(data):
    """Tabel 1: Toate datele detaliate"""
    filepath = os.path.join(OUTPUT_DIR, "tabel_1_detaliat.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["N", "Algoritm", "Cost", "Timp (s)"])
        
        for n in sorted(data.keys()):
            for alg, cost, time_val in data[n]:
                writer.writerow([n, alg, f"{cost:.2f}", f"{time_val:.4f}"])
    print("-> Generat tabel_1_detaliat.csv")

def save_table_summary(data, best_known):
    """Tabel 2: Sumar Calitate (Gap Mediu)"""
    filepath = os.path.join(OUTPUT_DIR, "tabel_2_calitate.csv")
    gaps = defaultdict(list)

    for n, entries in data.items():
        opt = best_known[n]
        for alg, cost, _ in entries:
            gap = 100 * (cost - opt) / opt
            gaps[alg].append(gap)
            
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritm", "Eroare Medie (%)", "Eroare Maxima (%)"])
        for alg, values in gaps.items():
            if alg == "Held-Karp": continue
            avg_gap = sum(values) / len(values)
            max_gap = max(values)
            writer.writerow([alg, f"{avg_gap:.2f}%", f"{max_gap:.2f}%"])
    print("-> Generat tabel_2_calitate.csv")

def save_table_scalability(data):
    """Tabel 3: Scalabilitate (Timpul la N=Max vs N=Min)"""
    filepath = os.path.join(OUTPUT_DIR, "tabel_3_scalabilitate.csv")
    ns = sorted(data.keys())
    if not ns: return
    
    min_n, max_n = ns[0], ns[-1]
    
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algoritm", f"Timp la N={min_n} (s)", f"Timp la N={max_n} (s)", "Factor Crestere"])
        
        # Facem un dict rapid pentru lookup
        times = defaultdict(dict)
        for n in [min_n, max_n]:
            for alg, _, t in data[n]:
                times[alg][n] = t
                
        for alg in times.keys():
            t_min = times[alg].get(min_n, 0)
            t_max = times[alg].get(max_n, 0)
            if t_min > 0:
                factor = f"{t_max / t_min:.1f}x"
            else:
                factor = "-"
            writer.writerow([alg, f"{t_min:.4f}", f"{t_max:.4f}", factor])
    print("-> Generat tabel_3_scalabilitate.csv")

if __name__ == "__main__":
    # Creare folder output dacă nu există
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    data = load_results(RESULTS_FILE)
    if not data:
        print("Nu există date de analizat. Rulați run_tests.py mai întâi.")
    else:
        best_known = get_best_solutions(data)
        
        # Generare Grafice
        plot_time(data)
        plot_quality_gap(data, best_known)
        plot_bar_comparison(data, target_n=100) # Poți schimba N-ul aici
        
        # Generare Tabele
        save_table_detailed(data)
        save_table_summary(data, best_known)
        save_table_scalability(data)
        
        print("\nAnaliză completă! Verificați folderul 'results/' pentru fișiere.")