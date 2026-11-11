import random
import hashlib
from collections import Counter

# Фиксируем seed для воспроизводимости результатов
random.seed(42)

N, Q, SHARDS = 12000, 30000, 3

# user_id изменен на customer_id, event_id на order_id
rows = [
    dict(
        customer_id=i % 2500,  # 2500 уникальных клиентов (кардинальность 2500)
        category=i % 5,  # 5 категорий товаров (низкая кардинальность)
        order_id=i,  # монотонный идентификатор заказа
    )
    for i in range(N)
]


def stable_hash(value):
    digest = hashlib.sha256(str(value).encode()).digest()
    return int.from_bytes(digest[:8], "big")

def low_card(row):
    return row["category"] % SHARDS


def hashed_customer(row):
    return stable_hash(row["customer_id"]) % SHARDS


def range_order(row):
    return min(row["order_id"] // (N // SHARDS), SHARDS - 1)


def describe(name, assign, requests):
    docs = Counter(assign(r) for r in rows)
    load = Counter(assign(r) for r in requests)
    d = [docs[i] for i in range(SHARDS)]
    q = [load[i] for i in range(SHARDS)]

    print(f"--- {name} ---")
    print(
        f"  docs: {d}, queries: {q},"
        f" doc_max_mean={round(max(d) / (sum(d) / SHARDS), 2)},"
        f" query_max_mean={round(max(q) / (sum(q) / SHARDS), 2)}"
    )


uniform = random.choices(rows, k=Q)

hot_rows = [r for r in rows if r["category"] == 0]
hot = [
    (
        random.choice(hot_rows)
        if random.random() < 0.6
        else random.choice(rows)
    )
    for _ in range(Q)
]

# Запуск симуляции
for name, fn in [
    ("category", low_card),
    ("hashed_customer", hashed_customer),
    ("range_order", range_order),
]:
    describe(name + "/uniform", fn, uniform)
    describe(name + "/hot", fn, hot)
