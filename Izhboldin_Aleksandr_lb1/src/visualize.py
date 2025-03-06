from squaring import *
import time
import matplotlib.pyplot as plt

def benchmark_squaring(n: int) -> float:
    start = time.perf_counter()
    solve_squaring(n)
    end = time.perf_counter()
    return end - start


def plot_time_dependency(sizes: list[int]):
    times = []
    for n in sizes:
        t = benchmark_squaring(n)
        times.append(t)
        print(f"Размер квадрата n = {n}, время = {t:.4f} сек")

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, times, marker='o', linestyle='-', color='b')

    plt.yscale("log")
    plt.xlabel('Размер квадрата n')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Зависимость времени выполнения от размера квадрата')
    plt.xticks(sizes)
    plt.grid(True)
    plt.show()


# Пример использования:
if __name__ == '__main__':
    primes = [x for x in range(2, 42) if x == get_div(x)]
    sizes = [x for x in range(2, 42)]
    plot_time_dependency(primes)
