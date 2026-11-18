import random
from pymongo import MongoClient

# Зафиксируем seed для полной воспроизводимости данных
random.seed(42)

# Подключение к локальной MongoDB
client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
coll = client.nosql_lab12.courses

# Очистка коллекции перед генерацией
coll.drop()

# Генерация 5000 синтетических документов (Вариант 01)
rows = [{
    "departmentId": random.randint(1, 20),
    "semester": random.randint(1, 8),
    "title": f"Course {i}",
    "credits": random.randint(2, 6),
    "teacherId": random.randint(1, 150)
} for i in range(5000)]

coll.insert_many(rows)
print("Успешно сгенерировано документов:", coll.count_documents({}))
