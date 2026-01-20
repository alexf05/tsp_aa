# Analiza Comparativă a Algoritmilor pentru Problema Comisului Voiajor (TSP)

Acest proiect implementează și compară performanța a patru algoritmi distincți pentru rezolvarea **Problemei Comisului Voiajor** (Traveling Salesperson Problem – **TSP**). Analiza se concentrează pe compromisul dintre **timpul de execuție** și **calitatea soluției** obținute, variind dimensiunea instanțelor de la **N = 10** până la **N = 500** orașe.

---

## 📂 Structura Proiectului

```text
.
├── data/random/           # Fișierele de intrare generate (instanțe TSP)
├── results/               # Rezultatele testelor (CSV) și graficele generate (PNG)
├── scripts/               # Scripturi pentru automatizare
│   ├── generate_data.py   # Generare instanțe aleatoare
│   ├── run_tests.py       # Rulare benchmark-uri
│   └── analyze_results.py # Analiză date și generare grafice
├── src/                   # Implementarea algoritmilor
│   ├── nearest_neighbor.py
│   ├── two_opt.py
│   ├── simulated_annealing.py
│   └── held_karp.py
└── utils.py               # Funcții utilitare (calcul distanțe, cost total)
```

---

## 🚀 Algoritmi Implementați

* **Nearest Neighbor (NN)**
  Algoritm greedy, foarte rapid, utilizat ca soluție inițială pentru alte metode de optimizare.

* **Held-Karp**
  Algoritm exact bazat pe programare dinamică. Găsește optimul global, dar are complexitate exponențială și este rulat doar pentru **N ≤ 20**.

* **2-Opt**
  Algoritm de căutare locală care îmbunătățește o soluție existentă prin eliminarea încrucișărilor din traseu.

* **Simulated Annealing (SA)**
  Meta-euristică probabilistică inspirată din procesul de recoacere a metalelor, capabilă teoretic să evadeze din optime locale.

---

## 🛠️ Instalare și Utilizare

Pentru rularea proiectului este necesar **Python 3**, împreună cu următoarele biblioteci:

```bash
pip install matplotlib numpy
```

### 1. Generarea Datelor

Generați seturi de date aleatoare pentru diferite dimensiuni ale problemei (10, 15, 20, 50, 100, 500 orașe):

```bash
python3 scripts/generate_data.py
```

### 2. Rularea Testelor

Executați algoritmii pe datele generate. Rezultatele brute vor fi salvate în `results/results.csv`.

> **Notă:** Algoritmul **Held-Karp** este rulat doar pentru instanțe mici (**N ≤ 20**) din cauza timpului mare de execuție.

```bash
python3 scripts/run_tests.py
```

### 3. Analiza Rezultatelor

Generați tabele, grafice și statistici bazate pe rulările anterioare. Fișierele rezultate vor fi salvate în folderul `results/`.

```bash
python3 scripts/analyze_results.py
```

---

## 📊 Analiza Rezultatelor și Concluzii

În urma testelor efectuate, s-au desprins câteva observații cheie privind comportamentul algoritmilor:

### 1. Compromisul Timp–Calitate

Algoritmul **2-Opt** s-a dovedit a fi cel mai performant din punct de vedere calitativ pentru instanțele mari, reducând eroarea medie la **sub 5%** față de soluția de referință. Acest câștig de calitate vine însă cu un **timp de execuție mai ridicat** comparativ cu heuristica simplă **Nearest Neighbor**.

### 2. Sensibilitatea Meta-euristicilor (Simulated Annealing)

O observație notabilă este performanța algoritmului **Simulated Annealing**. Pentru instanțele de **N = 100** și **N = 500**, acesta a produs rezultate **identice** cu soluția inițială oferită de **Nearest Neighbor** (utilizată pentru inițializare).

**Interpretare:**
Aceasta indică faptul că, în configurația curentă, schema de răcire a fost prea agresivă (parametrii `alpha` sau temperatura inițială `T` nu au fost calibrați optim). Algoritmul a „înghețat” prea rapid, fiind împiedicat să exploreze soluții temporar mai slabe și să evadeze din optimul local inițial. Rezultatul confirmă necesitatea **calibrării atente a parametrilor** pentru meta-euristici, în special pentru instanțe de dimensiuni mari.

### 3. Scalabilitate

* **Held-Karp** devine impracticabil pentru **N > 20**, timpul de execuție crescând exponențial.
* **Nearest Neighbor** este extrem de rapid și scalează foarte bine, dar oferă soluții cu erori relativ mari (**15–20%**).
* **2-Opt** oferă cel mai bun compromis pentru aplicații practice, unde calitatea traseului este prioritară, dar timpul de calcul trebuie să rămână rezonabil.

---

## 📈 Vizualizări

Scriptul de analiză generează următoarele grafice în folderul `results/`:

* `grafic_1_timp.png` – comparație a timpilor de execuție (scară logaritmică)
* `grafic_2_calitate.png` – deviația procentuală față de optim
* `grafic_3_bar_chart.png` – comparație directă a costurilor pentru **N = 100**

---

## 🎓 Context Academic

Acest proiect a fost realizat în cadrul cursului de **Analiza Algoritmilor** și are ca scop evidențierea diferențelor practice dintre algoritmi exacți, euristici și meta-euristici pentru problema TSP.

---

## ✍️ Autori

* **Fechet Alex-Ciprian**
* **Cazan Rares-Ștefan**
* **Petreus David-Mihai**

**Grupa:** 324CA
**Data:** Ianuarie 2026
**Instituție:** Facultatea de Automatică și Calculatoare, Universitatea Politehnica din București
