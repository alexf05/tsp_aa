import random
import os

def generate_points(n, filename):
    points = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(n)]
    with open(filename, "w") as f:
        f.write(str(n) + "\n")
        for x, y in points:
            f.write(f"{x} {y}\n")

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "../data/random")
    os.makedirs(data_dir, exist_ok=True)

    for n in [10, 15, 20, 50, 100, 500]:
        filepath = os.path.join(data_dir, f"tsp_{n}.txt")
        generate_points(n, filepath)