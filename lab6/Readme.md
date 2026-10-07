ОТЧЕТ ПО ЛАБОРАТОРНОЙ РАБОТЕ № 6

Дисциплина: Проектирование и применение NoSQL-технологий

Тема: Моделирование таблиц Cassandra от запросов (реализация паттернов Query-Driven Design в СУБД MongoDB)

Вариант: № 1 — Университет

1. Цель работы

Сформировать практические навыки query-driven проектирования NoSQL-модели: от анализа пользовательских запросов и нагрузки к выбору аналогов partition key и clustering columns (составных индексов), созданию коллекций и проверке того, что ключевые запросы выполняются без полного сканирования коллекции (Full Collection Scan).

2. Описание предметной области и карта запросов

Рассматривается информационная система университета. Для обеспечения высоких показателей производительности чтения модель проектируется отдельно под каждый из 5 ключевых паттернов доступа.

Карта запросов (Query-Driven Matrix)

№

Запрос (Access Pattern)

Известно на входе

Analog Partition Key

Analog Clustering Columns

Коллекция MongoDB

Q1

Расписание конкретной группы

group_id

group_id

lesson_date, lesson_time

schedule_by_group

Q2

Расписание группы за период

group_id, lesson_date (диапазон)

group_id

lesson_date, lesson_time

schedule_by_group

Q3

Занятия конкретного преподавателя

teacher_id

teacher_id

lesson_date, lesson_time

schedule_by_teacher

Q4

Занятия преподавателя за период

teacher_id, lesson_date (диапазон)

teacher_id

lesson_date, lesson_time

schedule_by_teacher

Q5

Занятие группы в конкретные дату и время

group_id, lesson_date, lesson_time

group_id

lesson_date, lesson_time

schedule_by_group

3. Проектирование и создание структуры данных

В соответствии с концепциями NoSQL, под разные шаблоны чтения создаются две денормализованные коллекции с составными индексами (Compound Indexes), выполняющими роль PRIMARY KEY ((Partition Key), Clustering Columns).

3.1. Создание базы данных и коллекций

use lab6_university;

db.createCollection("schedule_by_group");
db.createCollection("schedule_by_teacher");


<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/fa04ed0c-7672-4a9b-9452-51fe644e5fc6" />


3.2. Настройка индексов (Аналог Partition Key + Clustering Columns)

// Индекс для schedule_by_group: { PartitionKey: 1, Clustering1: 1, Clustering2: 1 }
db.schedule_by_group.createIndex(
  { group_id: 1, lesson_date: 1, lesson_time: 1 },
  { name: "pk_group_schedule" }
);

// Индекс для schedule_by_teacher: { PartitionKey: 1, Clustering1: 1, Clustering2: 1 }
db.schedule_by_teacher.createIndex(
  { teacher_id: 1, lesson_date: 1, lesson_time: 1 },
  { name: "pk_teacher_schedule" }
);


<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/2320cfa2-10ff-4328-9376-684144d0584b" />


4. Наполнение тестовыми данными

Выполнена запись 20+ документов с распределением по разным группам и преподавателям для проверки изоляции партиций.

// Вставка в коллекцию schedule_by_group
db.schedule_by_group.insertMany([
  { group_id: "IS-24-1", lesson_date: ISODate("2026-10-12"), lesson_time: "09:00", course_id: "CS-101", course_name: "NoSQL Databases", teacher_id: "T-10", teacher_name: "A. Petrov", room: "301" },
  { group_id: "IS-24-1", lesson_date: ISODate("2026-10-12"), lesson_time: "10:45", course_id: "CS-102", course_name: "Web Programming", teacher_id: "T-11", teacher_name: "B. Ivanov", room: "405" },
  { group_id: "IS-24-1", lesson_date: ISODate("2026-10-13"), lesson_time: "09:00", course_id: "CS-103", course_name: "Software Architecture", teacher_id: "T-10", teacher_name: "A. Petrov", room: "301" },
  { group_id: "IS-24-1", lesson_date: ISODate("2026-10-13"), lesson_time: "12:30", course_id: "CS-104", course_name: "Algorithms", teacher_id: "T-12", teacher_name: "C. Sidorov", room: "210" },
  { group_id: "IS-24-1", lesson_date: ISODate("2026-10-14"), lesson_time: "09:00", course_id: "CS-101", course_name: "NoSQL Databases", teacher_id: "T-10", teacher_name: "A. Petrov", room: "301" },
  { group_id: "CS-24-2", lesson_date: ISODate("2026-10-12"), lesson_time: "09:00", course_id: "CS-104", course_name: "Algorithms", teacher_id: "T-12", teacher_name: "C. Sidorov", room: "210" },
  { group_id: "CS-24-2", lesson_date: ISODate("2026-10-12"), lesson_time: "10:45", course_id: "CS-101", course_name: "NoSQL Databases", teacher_id: "T-10", teacher_name: "A. Petrov", room: "302" },
  { group_id: "CS-24-2", lesson_date: ISODate("2026-10-13"), lesson_time: "09:00", course_id: "CS-102", course_name: "Web Programming", teacher_id: "T-11", teacher_name: "B. Ivanov", room: "405" },
  { group_id: "CS-24-2", lesson_date: ISODate("2026-10-14"), lesson_time: "14:00", course_id: "CS-105", course_name: "Machine Learning", teacher_id: "T-13", teacher_name: "D. Kasenov", room: "101" },
  { group_id: "CS-24-2", lesson_date: ISODate("2026-10-15"), lesson_time: "09:00", course_id: "CS-105", course_name: "Machine Learning", teacher_id: "T-13", teacher_name: "D. Kasenov", room: "101" }
]);

// Денормализованная вставка в коллекцию schedule_by_teacher
db.schedule_by_teacher.insertMany([
  { teacher_id: "T-10", lesson_date: ISODate("2026-10-12"), lesson_time: "09:00", group_id: "IS-24-1", course_id: "CS-101", course_name: "NoSQL Databases", room: "301" },
  { teacher_id: "T-11", lesson_date: ISODate("2026-10-12"), lesson_time: "10:45", group_id: "IS-24-1", course_id: "CS-102", course_name: "Web Programming", room: "405" },
  { teacher_id: "T-10", lesson_date: ISODate("2026-10-13"), lesson_time: "09:00", group_id: "IS-24-1", course_id: "CS-103", course_name: "Software Architecture", room: "301" },
  { teacher_id: "T-12", lesson_date: ISODate("2026-10-13"), lesson_time: "12:30", group_id: "IS-24-1", course_id: "CS-104", course_name: "Algorithms", room: "210" },
  { teacher_id: "T-10", lesson_date: ISODate("2026-10-14"), lesson_time: "09:00", group_id: "IS-24-1", course_id: "CS-101", course_name: "NoSQL Databases", room: "301" },
  { teacher_id: "T-12", lesson_date: ISODate("2026-10-12"), lesson_time: "09:00", group_id: "CS-24-2", course_id: "CS-104", course_name: "Algorithms", room: "210" },
  { teacher_id: "T-10", lesson_date: ISODate("2026-10-12"), lesson_time: "10:45", group_id: "CS-24-2", course_id: "CS-101", course_name: "NoSQL Databases", room: "302" },
  { teacher_id: "T-11", lesson_date: ISODate("2026-10-13"), lesson_time: "09:00", group_id: "CS-24-2", course_id: "CS-102", course_name: "Web Programming", room: "405" },
  { teacher_id: "T-13", lesson_date: ISODate("2026-10-14"), lesson_time: "14:00", group_id: "CS-24-2", course_id: "CS-105", course_name: "Machine Learning", room: "101" },
  { teacher_id: "T-13", lesson_date: ISODate("2026-10-15"), lesson_time: "09:00", group_id: "CS-24-2", course_id: "CS-105", course_name: "Machine Learning", room: "101" }
]);


<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/eb7d3d9e-2ff6-4914-a258-b6ed6bb75fc6" />


5. Выполнение 5 обязательных запросов (SELECT / FIND)

Запрос Q1: Расписание группы IS-24-1

db.schedule_by_group.find({ group_id: "IS-24-1" }).sort({ lesson_date: 1, lesson_time: 1 });


<img width="1421" height="889" alt="image" src="https://github.com/user-attachments/assets/7401f261-3590-4343-888f-f427ab016203" />


Запрос Q2: Расписание группы IS-24-1 за период (12–13 октября 2026)

db.schedule_by_group.find({
  group_id: "IS-24-1",
  lesson_date: {
    $gte: ISODate("2026-10-12"),
    $lte: ISODate("2026-10-13")
  }
}).sort({ lesson_date: 1, lesson_time: 1 });


<img width="845" height="898" alt="image" src="https://github.com/user-attachments/assets/ada18dbc-17d4-4185-bc5c-ceb0bf1a5ebf" />


Запрос Q3: Занятия преподавателя A. Petrov (T-10)

db.schedule_by_teacher.find({ teacher_id: "T-10" }).sort({ lesson_date: 1, lesson_time: 1 });


<img width="967" height="886" alt="image" src="https://github.com/user-attachments/assets/03ea1af6-b12e-4e16-9089-a81675d3fdf3" />


Запрос Q4: Занятия преподавателя T-10 за период (12–13 октября 2026)

db.schedule_by_teacher.find({
  teacher_id: "T-10",
  lesson_date: {
    $gte: ISODate("2026-10-12"),
    $lte: ISODate("2026-10-13")
  }
}).sort({ lesson_date: 1, lesson_time: 1 });


<img width="794" height="892" alt="image" src="https://github.com/user-attachments/assets/a137bb77-6c26-4df3-a574-2e1be48b02ae" />


Запрос Q5: Занятие группы IS-24-1 на конкретную дату и время

db.schedule_by_group.find({
  group_id: "IS-24-1",
  lesson_date: ISODate("2026-10-12"),
  lesson_time: "09:00"
});


<img width="504" height="384" alt="image" src="https://github.com/user-attachments/assets/104b902b-2826-4283-8115-d7c87b0bca92" />

6. Операции изменения (UPDATE) и удаления (DELETE)

При обновлении и удалении в денормализованной NoSQL-структуре строго соблюдается модификация данных во всех представлениях.

6.1. Изменение аудитории (UPDATE)

Переносим занятие группы IS-24-1 от 12.10.2026 09:00 в аудиторию 505:

// 1. Обновление в представлении группы
db.schedule_by_group.updateOne(
  { group_id: "IS-24-1", lesson_date: ISODate("2026-10-12"), lesson_time: "09:00" },
  { $set: { room: "505" } }
);

// 2. Синхронное обновление в представлении преподавателя
db.schedule_by_teacher.updateOne(
  { teacher_id: "T-10", lesson_date: ISODate("2026-10-12"), lesson_time: "09:00" },
  { $set: { room: "505" } }
);


<img width="851" height="259" alt="image" src="https://github.com/user-attachments/assets/116061b7-de98-43b4-a860-ea24896ad022" />


6.2. Удаление тестовой записи (DELETE)

Удаляем занятие группы CS-24-2 от 15.10.2026 09:00:

// 1. Удаление из schedule_by_group
db.schedule_by_group.deleteOne({
  group_id: "CS-24-2",
  lesson_date: ISODate("2026-10-15"),
  lesson_time: "09:00"
});

// 2. Удаление из schedule_by_teacher
db.schedule_by_teacher.deleteOne({
  teacher_id: "T-13",
  lesson_date: ISODate("2026-10-15"),
  lesson_time: "09:00"
});


<img width="340" height="232" alt="image" src="https://github.com/user-attachments/assets/cb5d3e14-69d9-42ec-b2e2-f895ce2ad9ad" />


7. Аналитический расчет роста партиций и Time Bucketing

Анализ объема данных

Исходные параметры: 4 пары/день, 6 учебных дней в неделю, 15 недель в семестре, 8 семестров за бакалавриат.

Расчет для одной группы (group_id):

$$\text{Записей за семестр} = 4 \times 6 \times 15 = 360 \text{ документов}$$

$$\text{Записей за 4 года обучения} = 360 \times 8 = 2880 \text{ документов}$$

Оценка риска: Объем 2880 документов на группу полностью безопасен и умещается в лимиты памяти.

Альтернативная модель с Time Bucketing (Повышенный уровень)

Для преподавателей с большим стажем (10+ лет) или при высокой частоте занятий возможен риск переполнения партиции/индекса. Решением является Time Bucketing (добавление учебного года academic_year в составной ключ):

// Добавление бакета года в структуру коллекции
db.schedule_by_teacher_bucketed.createIndex({
  teacher_id: 1,
  academic_year: 1, // Time Bucket (например: 2026)
  lesson_date: 1,
  lesson_time: 1
});


8. Ответы на контрольные вопросы

Что означает query-driven design в NoSQL?

Это проектирование базы данных от готовых пользовательских запросов (SELECT), а не от сущностей предметной области.

Какую роль выполняет partition key (первый элемент составного индекса)?

Определяет логическую группировку данных (группу или преподавателя) и обеспечивает адресную адресацию при поиске.

Чем clustering column отличается от partition key?

Clustering column задает порядок сортировки документов внутри одной группы/партиции.

Почему запрос без partition key указывает на проблему модели?

Запрос без партиционного ключа приводит к сканированию всей базы данных (Full Collection/Cluster Scan), что снижает производительность.

Почему допустима денормализация?

Из-за отсутствия быстрых распределенных JOIN. Дублирование данных — компромисс ради быстрого чтения за один запрос.

9. Вывод

В ходе лабораторной работы освоены принципы проектирования NoSQL-систем от паттернов доступа (Query-Driven Design). Спроектированы и реализованы две денормализованные структуры данных, обеспечивающие выполнение всех основных запросов без полного сканирования коллекции. Проведена оценка роста объема данных и предложен метод Time Bucketing для предотвращения аномалий роста партиций.
