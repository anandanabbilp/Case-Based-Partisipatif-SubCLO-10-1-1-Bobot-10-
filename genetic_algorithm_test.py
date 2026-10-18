"""
TUGAS CASE-BASED PROGRAMMING - GENETIC ALGORITHM
Nama  : Ananda Nabbil Pratama
Kelas : IF-48-02PJJ
NIM   : 103042400052
"""

import math
import random

#Setting batas bawah dan batas atas domain x1 (atau x) dan x2 (atau y)
DOMAIN_X1 = (-5.0, 5.0)  # Contoh: rentang domain -5 <= x1 <= 5
DOMAIN_X2 = (-5.0, 5.0)  # Contoh: rentang domain -5 <= x2 <= 5

def fungsi_objektif(x1: float, x2: float) -> float:
    """
    Masukkan rumus fungsi yang ingin dicari nilai maksimumnya di sini.
    Contoh saat ini: f(x1, x2) = (cos(x1) + sin(x2))^2 / (x1^2 + x2^2 + 1)
    Ganti baris return di bawah dengan rumus pada soal Anda.
    """
    return ((math.cos(x1) + math.sin(x2)) ** 2) / (x1**2 + x2**2 + 1.0)


#SETTING PARAMETER GENETIC ALGORITHM (GA)
POPULATION_SIZE = 100     # Jumlah individu (kromosom) dalam satu generasi
GENERATIONS = 150         # Jumlah iterasi generasi maksimum
CROSSOVER_RATE = 0.85     # Probabilitas terjadinya pindah silang (crossover)
MUTATION_RATE = 0.15      # Probabilitas terjadinya mutasi pada gen
MUTATION_STEP = 0.25      # Standar deviasi perubahan nilai saat mutasi
TOURNAMENT_SIZE = 3       # Ukuran turnamen untuk seleksi induk (parent)
ELITISM_COUNT = 2         # Jumlah individu terbaik yang langsung dipertahankan
RANDOM_SEED = 42          # Seed agar hasil eksekusi konsisten dan dapat diuji ulang


#IMPLEMENTASI TAHAPAN GENETIC ALGORITHM (BUILD FROM SCRATCH)
def inisialisasi_populasi(pop_size: int, dom_x1: tuple, dom_x2: tuple) -> list:
    """Membangkitkan populasi awal secara acak di dalam rentang domain."""
    populasi = []
    for _ in range(pop_size):
        x1 = random.uniform(dom_x1[0], dom_x1[1])
        x2 = random.uniform(dom_x2[0], dom_x2[1])
        populasi.append([x1, x2])
    return populasi


def hitung_fitness(individu: list) -> float:
    """Menghitung nilai fitness (karena mencari nilai maksimum, fitness = f(x1, x2))."""
    return fungsi_objektif(individu[0], individu[1])


def seleksi_turnamen(populasi: list, fitness_list: list, k: int) -> list:
    """Memilih satu induk terbaik dari k sampel acak menggunakan Tournament Selection."""
    indeks_kandidat = random.sample(range(len(populasi)), k)
    indeks_terbaik = max(indeks_kandidat, key=lambda idx: fitness_list[idx])
    return populasi[indeks_terbaik][:]


def crossover_aritmatika(induk1: list, induk2: list, pc: float) -> tuple:
    """Melakukan pindah silang (Arithmetic Crossover) antara dua induk."""
    if random.random() < pc:
        alpha = random.random()
        anak1 = [
            alpha * induk1[0] + (1.0 - alpha) * induk2[0],
            alpha * induk1[1] + (1.0 - alpha) * induk2[1],
        ]
        anak2 = [
            (1.0 - alpha) * induk1[0] + alpha * induk2[0],
            (1.0 - alpha) * induk1[1] + alpha * induk2[1],
        ]
        return anak1, anak2
    return induk1[:], induk2[:]


def mutasi_gaussian(individu: list, pm: float, step: float, dom_x1: tuple, dom_x2: tuple) -> list:
    """Melakukan mutasi Gaussian dan memastikan nilai gen tetap di dalam batas domain."""
    hasil = individu[:]
    if random.random() < pm:
        hasil[0] += random.gauss(0.0, step)
        hasil[0] = max(dom_x1[0], min(dom_x1[1], hasil[0]))
    if random.random() < pm:
        hasil[1] += random.gauss(0.0, step)
        hasil[1] = max(dom_x2[0], min(dom_x2[1], hasil[1]))
    return hasil


def jalankan_genetic_algorithm():
    """Fungsi utama untuk menjalankan siklus evolusi Genetic Algorithm."""
    random.seed(RANDOM_SEED)

    populasi = inisialisasi_populasi(POPULATION_SIZE, DOMAIN_X1, DOMAIN_X2)
    solusi_terbaik = None
    fitness_terbaik = -float("inf")

    print("=" * 72)
    print("        PROGRAM OPTIMASI MAKSIMUM FUNGSI - GENETIC ALGORITHM")
    print("=" * 72)
    print(f"Nama            : Ananda Nabbil Pratama")
    print(f"Kelas           : IF-48-02PJJ")
    print(f"NIM             : 103042400052")
    print("-" * 72)
    print(f"Domain x1       : [{DOMAIN_X1[0]}, {DOMAIN_X1[1]}]")
    print(f"Domain x2       : [{DOMAIN_X2[0]}, {DOMAIN_X2[1]}]")
    print(f"Ukuran Populasi : {POPULATION_SIZE} individu")
    print(f"Jumlah Generasi : {GENERATIONS} generasi")
    print(f"Crossover Rate  : {CROSSOVER_RATE}")
    print(f"Mutation Rate   : {MUTATION_RATE}")
    print("=" * 72)

    for gen in range(1, GENERATIONS + 1):
        fitness_list = [hitung_fitness(ind) for ind in populasi]

        # Urutkan populasi berdasarkan fitness tertinggi ke terendah
        pasangan_urut = sorted(
            zip(populasi, fitness_list), key=lambda item: item[1], reverse=True
        )

        if pasangan_urut[0][1] > fitness_terbaik:
            fitness_terbaik = pasangan_urut[0][1]
            solusi_terbaik = pasangan_urut[0][0][:]

        # Tampilkan log perkembangan setiap 25 generasi dan pada generasi pertama
        if gen == 1 or gen % 25 == 0 or gen == GENERATIONS:
            print(
                f"Generasi {gen:3d} | x1 = {solusi_terbaik[0]:10.6f} | "
                f"x2 = {solusi_terbaik[1]:10.6f} | Fitness Maks = {fitness_terbaik:10.6f}"
            )

        # Elitism: pertahankan individu terbaik ke generasi berikutnya
        populasi_baru = [item[0][:] for item in pasangan_urut[:ELITISM_COUNT]]

        # Reproduksi (Seleksi, Crossover, dan Mutasi)
        while len(populasi_baru) < POPULATION_SIZE:
            induk1 = seleksi_turnamen(populasi, fitness_list, TOURNAMENT_SIZE)
            induk2 = seleksi_turnamen(populasi, fitness_list, TOURNAMENT_SIZE)

            anak1, anak2 = crossover_aritmatika(induk1, induk2, CROSSOVER_RATE)

            anak1 = mutasi_gaussian(anak1, MUTATION_RATE, MUTATION_STEP, DOMAIN_X1, DOMAIN_X2)
            anak2 = mutasi_gaussian(anak2, MUTATION_RATE, MUTATION_STEP, DOMAIN_X1, DOMAIN_X2)

            populasi_baru.append(anak1)
            if len(populasi_baru) < POPULATION_SIZE:
                populasi_baru.append(anak2)

        populasi = populasi_baru

    print("=" * 72)
    print("HASIL AKHIR OPTIMASI GENETIC ALGORITHM:")
    print(f"  Titik Optimal (x1*, x2*) = ({solusi_terbaik[0]:.6f}, {solusi_terbaik[1]:.6f})")
    print(f"  Nilai Maksimum Fungsi    = {fitness_terbaik:.6f}")
    print("=" * 72)

    return solusi_terbaik, fitness_terbaik


# 4. UNIT TEST / PENGUJIAN OTOMATIS PROGRAM
def test_program_ga():
    """Fungsi untuk menguji kevalidan setiap komponen Genetic Algorithm."""
    print("\n[INFO] Menjalankan pengujian (Unit Test) komponen program...")

    # Test 1: Inisialisasi populasi berada di dalam batas domain
    pop = inisialisasi_populasi(20, DOMAIN_X1, DOMAIN_X2)
    assert len(pop) == 20, "Jumlah populasi tidak sesuai!"
    for x1, x2 in pop:
        assert DOMAIN_X1[0] <= x1 <= DOMAIN_X1[1], "Nilai x1 keluar dari batas domain!"
        assert DOMAIN_X2[0] <= x2 <= DOMAIN_X2[1], "Nilai x2 keluar dari batas domain!"

    # Test 2: Mutasi tidak melanggar batas domain (clamping bekerja)
    ind_uji = [DOMAIN_X1[1], DOMAIN_X2[0]]
    for _ in range(50):
        hasil_mutasi = mutasi_gaussian(ind_uji, 1.0, 10.0, DOMAIN_X1, DOMAIN_X2)
        assert DOMAIN_X1[0] <= hasil_mutasi[0] <= DOMAIN_X1[1], "Mutasi x1 melewati batas!"
        assert DOMAIN_X2[0] <= hasil_mutasi[1] <= DOMAIN_X2[1], "Mutasi x2 melewati batas!"

    # Test 3: Pastikan hasil GA mendekati nilai maksimum sebenarnya melalui Grid Search
    solusi_ga, maks_ga = jalankan_genetic_algorithm()
    maks_grid = -float("inf")
    langkah = 200
    for i in range(langkah + 1):
        u = DOMAIN_X1[0] + (DOMAIN_X1[1] - DOMAIN_X1[0]) * i / langkah
        for j in range(langkah + 1):
            v = DOMAIN_X2[0] + (DOMAIN_X2[1] - DOMAIN_X2[0]) * j / langkah
            maks_grid = max(maks_grid, fungsi_objektif(u, v))

    selisih = abs(maks_ga - maks_grid)
    print(f"[TEST] Nilai Maksimum Referensi (Grid Search) : {maks_grid:.6f}")
    print(f"[TEST] Nilai Maksimum Genetic Algorithm       : {maks_ga:.6f}")
    print(f"[TEST] Selisih Error                          : {selisih:.6f}")
    assert maks_ga >= maks_grid - 1e-2, "GA belum konvergen ke nilai maksimum global!"
    print("[PASS] Semua pengujian (Unit Test & Verifikasi Konvergensi) BERHASIL!\n")


if __name__ == "__main__":
    test_program_ga()