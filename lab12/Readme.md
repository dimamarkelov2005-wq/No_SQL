# Лабораторная работа №12: Разработка и запуск воспроизводимого benchmark-сценария

- **Дисциплина:** Проектирование и применение NoSQL-технологий
- **Вариант:** 01 (Каталог курсов. Фильтр: `departmentId + semester`)
- **Студент:** [Маркелов Дмитрий, ИС_24-21]

---

## 1. Цель и результаты
Разработка воспроизводимого эксперимента производительности NoSQL-подсистемы (MongoDB), измерение `latency`, `throughput` и ошибок, сравнение базовой (Baseline) и оптимизированной конфигураций индексов, научное обоснование выводов.

## 2. Окружение и версии
- **СУБД:** MongoDB 7.x / Local standalone instance
- **Язык программирования:** Python 3.10+
- **Используемые библиотеки:** `pymongo`, `pandas`, `matplotlib`
- **Количество документов:** 5000 синтетических документов (`seed = 42`)

## 3. Схема данных и гипотеза
- **Коллекция:** `courses`
- **Документ:** `{"departmentId": int, "semester": int, "title": str, "credits": int, "teacherId": int}`
- **Гипотеза:** Создание составного индекса `{ departmentId: 1, semester: 1 }` переведет план запроса с полного сканирования коллекции (`COLLSCAN`) на сканирование по индексу (`IXSCAN`), что существенно снизит метрику P95 задержки чтения и уменьшит число просмотренных документов (`totalDocsExamined`).

## 4. Анализ плана запроса (Explain)

### До индекса (Baseline):
<img width="1022" height="1031" alt="image" src="https://github.com/user-attachments/assets/359283c2-e9f9-43de-b556-d4749dd9b769" />
<img width="802" height="705" alt="image" src="https://github.com/user-attachments/assets/a0d78c9c-2dd5-4385-818e-fa08649dfee7" />


- `stage`: `COLLSCAN`
- `totalDocsExamined`: 5000
- `executionTimeMillis`: ~15-25 ms

### После создания индекса:
<img width="802" height="1028" alt="image" src="https://github.com/user-attachments/assets/f9fddc42-8a51-4e90-80d1-d08e3fb9240c" />
<img width="862" height="1029" alt="image" src="https://github.com/user-attachments/assets/7614c0e8-4705-4613-aa7b-d638cb950221" />
<img width="641" height="312" alt="image" src="https://github.com/user-attachments/assets/d8af1215-6dae-4f8a-b693-8df1cdc29af0" />


- `stage`: `IXSCAN` (`executionStats.executionStages.stage`)
- `totalDocsExamined`: Сократилось до реального числа найденных документов.
- `executionTimeMillis`: Уменьшилось до < 2 ms.

---

## 5. Таблица результатов эксперимента

| Режим | Клиенты (Workers) | Повтор | RPS (Throughput) | P50 (ms) | P95 (ms) | P99 (ms) | Ошибки |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Без индекса | 1 | 1-3 | 310.45 | 2.81 | 5.20 | 8.12 | 0 |
| Без индекса | 4 | 1-3 | 680.12 | 5.10 | 14.50 | 22.30 | 0 |
| Без индекса | 8 | 1-3 | 715.40 | 9.80 | 28.40 | 45.10 | 0 |
| С индексом | 1 | 1-3 | 850.20 | 1.05 | 1.80 | 2.90 | 0 |
| С индексом | 4 | 1-3 | 2150.80 | 1.65 | 3.20 | 5.40 | 0 |
| С индексом | 8 | 1-3 | 2400.10 | 2.90 | 6.10 | 10.20 | 0 |

---

## 6. Графики производительности
<img width="1049" height="703" alt="p95_chart" src="https://github.com/user-attachments/assets/199eb41b-73b3-4b3d-a028-e5d831457bfe" />

<img width="1055" height="703" alt="throughput_chart" src="https://github.com/user-attachments/assets/7b238b65-f120-4bc7-8578-3cf0c09afe6b" />


## 7. Анализ и расчеты
1. **Относительное улучшение P95:** 
   $$\text{Улучшение} = \frac{P95_{\text{до}} - P95_{\text{после}}}{P95_{\text{до}}} \times 100\% = \frac{28.40 - 6.10}{28.40} \times 100\% \approx 78.5\%$$
2. **Доля ошибок:** Составила `0%` во всех режимах, так как нагрузочный тест работал в стабильном `closed-loop` контуре с обработкой исключений сети.
3. **Плато Throughput:** При переходе от 4 к 8 клиентам пропускная способность (RPS) выходит на плато из-за ограничения ресурсов локального потока процессора и блокировок Питона (`GIL` / `ThreadPoolExecutor`).

## 8. Выводы
Гипотеза полностью подтвердилась. Внедрение составного индекса `{departmentId: 1, semester: 1}` исключило затратный `COLLSCAN`, снизив задержку P95 более чем в 4 раза и увеличив пропускную способность системы в ~3.3 раза.
