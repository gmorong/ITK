import random
import time
import json
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path


def generate_data(n):
    return [random.randint(100, 500) for _ in range(n)]


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def process_number(number):
    result = 0
    for _ in range(10000):
        for i in range(2, number):
            if is_prime(i):
                result += 1
    
    return {
        'number': number,
        'iterations': result,
        'is_prime': is_prime(number)
    }


def sequential_processing(data):
    start = time.time()
    results = [process_number(num) for num in data]
    elapsed = time.time() - start
    return results, elapsed


def variant_a_thread_pool(data):
    start = time.time()
    with ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
        results = list(executor.map(process_number, data))
    elapsed = time.time() - start
    return results, elapsed


def variant_b_process_pool(data):
    start = time.time()
    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        results = list(executor.map(process_number, data))
    elapsed = time.time() - start
    return results, elapsed


def worker_process(input_queue, output_queue):
    while True:
        item = input_queue.get()
        if item is None:
            break
        result = process_number(item)
        output_queue.put(result)


def variant_c_manual_processes(data):
    start = time.time()
    
    num_processes = mp.cpu_count()
    input_queue = mp.Queue()
    output_queue = mp.Queue()
    
    processes = []
    for _ in range(num_processes):
        p = mp.Process(target=worker_process, args=(input_queue, output_queue))
        p.start()
        processes.append(p)
    
    for num in data:
        input_queue.put(num)
    
    for _ in range(num_processes):
        input_queue.put(None)
    
    results = []
    for _ in range(len(data)):
        results.append(output_queue.get())
    
    for p in processes:
        p.join()
    
    elapsed = time.time() - start
    return results, elapsed


def save_performance_results(performance, filepath):
    with open(filepath, 'w') as f:
        json.dump(performance, f, indent=2)


def main():
    n = 20
    print(f"Генерация {n} чисел...")
    data = generate_data(n)
    
    print(f"Количество CPU: {mp.cpu_count()}\n")
    print("Запуск тестов производительности...\n")
    
    performance = {}
    
    print("1. Последовательная обработка...")
    results_seq, time_seq = sequential_processing(data)
    performance['sequential'] = {'time': time_seq, 'speedup': 1.0}
    print(f"   Время: {time_seq:.2f} сек\n")
    
    print("2. Вариант A: ThreadPoolExecutor...")
    results_a, time_a = variant_a_thread_pool(data)
    performance['variant_a_threads'] = {'time': time_a, 'speedup': time_seq / time_a}
    print(f"   Время: {time_a:.2f} сек\n")
    
    print("3. Вариант B: ProcessPoolExecutor...")
    results_b, time_b = variant_b_process_pool(data)
    performance['variant_b_process_pool'] = {'time': time_b, 'speedup': time_seq / time_b}
    print(f"   Время: {time_b:.2f} сек\n")
    
    print("4. Вариант C: Manual Processes + Queue...")
    results_c, time_c = variant_c_manual_processes(data)
    performance['variant_c_manual_processes'] = {'time': time_c, 'speedup': time_seq / time_c}
    print(f"   Время: {time_c:.2f} сек\n")
    
    print("="*70)
    print("РЕЗУЛЬТАТЫ СРАВНЕНИЯ")
    print("="*70)
    print(f"{'Метод':<35} {'Время (сек)':<15} {'Ускорение'}")
    print("-"*70)
    
    for method, data in performance.items():
        print(f"{method:<35} {data['time']:>10.2f}      {data['speedup']:>6.2f}")
    
    script_dir = Path(__file__).parent
    
    perf_file = script_dir / 'results.json'
    save_performance_results(performance, perf_file)
    print(f"\nРезультаты производительности сохранены в {perf_file}")


if __name__ == '__main__':
    main()