from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
import statistics
import math
import csv
import os
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
coll = client.nosql_lab12.courses

# Запрос по Варианту 01 (фильтр: departmentId + semester)
QUERY = {"departmentId": 10, "semester": 5}

def one():
    start = perf_counter()
    try:
        list(coll.find(QUERY).limit(100))
        return ((perf_counter() - start) * 1000, True)
    except Exception:
        return ((perf_counter() - start) * 1000, False)

def percentile(v, p):
    v = sorted(v)
    if not v:
        return float("nan")
    idx = (len(v) - 1) * p / 100
    lo, hi = math.floor(idx), math.ceil(idx)
    return v[lo] + (v[hi] - v[lo]) * (idx - lo)

def run(workers=4, n=400):
    # Warm-up (прогрев пула соединений и кэша)
    for _ in range(40):
        one()
    
    t0 = perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda _: one(), range(n)))
    seconds = perf_counter() - t0
    
    lat = [res[0] for res in results if res[1]]
    success = len(lat)
    errors = n - success
    rps = success / seconds if seconds > 0 else 0
    
    return {
        "workers": workers,
        "success": success,
        "errors": errors,
        "rps": rps,
        "p50": percentile(lat, 50),
        "p95": percentile(lat, 95),
        "p99": percentile(lat, 99)
    }

if __name__ == "__main__":
    os.makedirs("charts", exist_ok=True)
    all_data = []
    
    # Тестирование для 1, 4 и 8 клиентов, по 3 повтора на каждый режим
    for workers in [1, 4, 8]:
        for repeat in range(1, 4):
            res = run(workers=workers, n=400)
            res["repeat"] = repeat
            print(f"Workers: {workers} | Repeat: {repeat} | RPS: {res['rps']:.2f} | P95: {res['p95']:.2f} ms")
            all_data.append(res)
            
    # Сохранение сырых данных в CSV
    keys = ["workers", "repeat", "rps", "p50", "p95", "p99", "errors", "success"]
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_data)
    print("Результаты успешно сохранены в results.csv")
