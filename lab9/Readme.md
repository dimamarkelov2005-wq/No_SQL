# Отчет по лабораторной работе №9
**Дисциплина:** Нереляционные базы данных (NoSQL)  
**Тема:** Создание графа в Neo4j и выполнение базовых запросов Cypher  
**Студент:** Маркелов Дмитрий  
**Курс / Специальность:** 3 курс, «Информационные системы»  
**Вариант:** № 1 (Предметная область: Университет)  

---

## 1. Цель работы
Освоить модель *Property Graph*, научиться создавать граф предметной области в СУБД Neo4j с помощью языка Cypher, выполнять поиск по шаблонам связей, производить фильтрацию, сортировку, изменять и безопасно удалять данные, а также предотвращать дублирование элементов с помощью механизмов уникальности и идемпотентности.

---

## 2. Краткое описание предметной области и схема графа

### Метки узлов (Nodes) и их свойства:
1. **`Student`** (Студент) — свойства: `id` (INTEGER, unique), `name` (STRING), `group` (STRING), `year` (INTEGER).
2. **`Course`** (Курс / Дисциплина) — свойства: `id` (INTEGER, unique), `title` (STRING), `credits` (INTEGER).
3. **`Teacher`** (Преподаватель) — свойства: `id` (INTEGER, unique), `name` (STRING), `department` (STRING).

### Типы отношений (Relationships) и их семантика:
1. **`(:Student)-[:STUDIES]->(:Course)`** — показывает, какой студент изучает данный курс (направлена от студента к курсу). Может содержать свойство `semester`.
2. **`(:Teacher)-[:TEACHES]->(:Course)`** — показывает, какой преподаватель читает данный курс (направлена от преподавателя к курсу).

---

## 3. Таблица элементов графа

| Тип элемента | Наименование / Метка | Описание свойства 1 | Описание свойства 2 | Описание свойства 3 |
| :--- | :--- | :--- | :--- | :--- |
| **Узел** | `Student` | `id` (Уникальный ИД) | `name` (ФИО студента) | `group` (Группа) |
| **Узел** | `Course` | `id` (Уникальный ИД) | `title` (Название предмета) | `credits` (Объем в кредитах) |
| **Узел** | `Teacher` | `id` (Уникальный ИД) | `name` (ФИО преподавателя) | `department` (Кафедра) |
| **Связь** | `STUDIES` | Направление: Student ➔ Course | Смысл: Изучение дисциплины | `semester` (Номер семестра) |
| **Связь** | `TEACHES` | Направление: Teacher ➔ Course | Смысл: Преподавание курса | — |

---

## 4. Выполнение заданий и Cypher-скрипты

### Задание 2. Создание ограничений и наполнение графа (12+ узлов, 15+ связей)
<img width="1300" height="524" alt="image" src="https://github.com/user-attachments/assets/fac91950-adda-4006-9a79-9e29cd0af59e" />
<img width="1699" height="864" alt="image" src="https://github.com/user-attachments/assets/659791f0-8d44-4f53-bb57-7ff20e6881b3" />

```cypher
// 1. Создание ограничений уникальности по id
CREATE CONSTRAINT student_id_unique IF NOT EXISTS FOR (s:Student) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT course_id_unique IF NOT EXISTS FOR (c:Course) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT teacher_id_unique IF NOT EXISTS FOR (t:Teacher) REQUIRE t.id IS UNIQUE;

// 2. Создание узлов (4 студента, 4 курса, 4 преподавателя)
MERGE (s1:Student {id: 1}) SET s1.name = "Aibek", s1.group = "IS-24-1", s1.year = 3;
MERGE (s2:Student {id: 2}) SET s2.name = "Aliya", s2.group = "IS-24-1", s2.year = 3;
MERGE (s3:Student {id: 3}) SET s3.name = "Damir", s3.group = "IS-24-2", s3.year = 2;
MERGE (s4:Student {id: 4}) SET s4.name = "Zhansaya", s4.group = "IS-24-2", s4.year = 2;

MERGE (c1:Course {id: 101}) SET c1.title = "NoSQL", c1.credits = 5;
MERGE (c2:Course {id: 102}) SET c2.title = "Algorithms", c2.credits = 4;
MERGE (c3:Course {id: 103}) SET c3.title = "Web Development", c3.credits = 5;
MERGE (c4:Course {id: 104}) SET c4.title = "Database Systems", c4.credits = 6;

MERGE (t1:Teacher {id: 201}) SET t1.name = "Dr. Smith", t1.department = "Computer Science";
MERGE (t2:Teacher {id: 202}) SET t2.name = "Prof. Johnson", t2.department = "Software Engineering";
MERGE (t3:Teacher {id: 203}) SET t3.name = "Dr. Davis", t3.department = "Information Systems";
MERGE (t4:Teacher {id: 204}) SET t4.name = "Prof. Wilson", t4.department = "Data Science";

// 3. Создание отношений (16 связей)
MATCH (s:Student {id: 1}), (c:Course {id: 101}) MERGE (s)-[:STUDIES]->(c);
MATCH (s:Student {id: 1}), (c:Course {id: 102}) MERGE (s)-[:STUDIES]->(c);
MATCH (s:Student {id: 2}), (c:Course {id: 101}) MERGE (s)-[:STUDIES]->(c);
MATCH (s:Student {id: 2}), (c:Course {id: 103}) MERGE (s)-[:STUDIES]->(c);
MATCH (s:Student {id: 3}), (c:Course {id: 102}) MERGE (s)-[:STUDIES]->(c);
MATCH (s:Student {id: 3}), (c:Course {id: 104}) MERGE (s)-[:STUDIES]->(c);
MATCH (s:Student {id: 4}), (c:Course {id: 103}) MERGE (s)-[:STUDIES]->(c);
MATCH (s:Student {id: 4}), (c:Course {id: 104}) MERGE (s)-[:STUDIES]->(c);

MATCH (t:Teacher {id: 201}), (c:Course {id: 101}) MERGE (t)-[:TEACHES]->(c);
MATCH (t:Teacher {id: 202}), (c:Course {id: 101}) MERGE (t)-[:TEACHES]->(c);
MATCH (t:Teacher {id: 202}), (c:Course {id: 102}) MERGE (t)-[:TEACHES]->(c);
MATCH (t:Teacher {id: 203}), (c:Course {id: 102}) MERGE (t)-[:TEACHES]->(c);
MATCH (t:Teacher {id: 203}), (c:Course {id: 103}) MERGE (t)-[:TEACHES]->(c);
MATCH (t:Teacher {id: 204}), (c:Course {id: 103}) MERGE (t)-[:TEACHES]->(c);
MATCH (t:Teacher {id: 201}), (c:Course {id: 104}) MERGE (t)-[:TEACHES]->(c);
MATCH (t:Teacher {id: 204}), (c:Course {id: 104}) MERGE (t)-[:TEACHES]->(c);

Задание 3. Выборка всех узлов метки, сортировка и ограничение
// Выборка всех узлов метки Student
MATCH (s:Student) 
RETURN s;

// Сортировка по имени и ограничение количества строк
MATCH (s:Student) 
RETURN s.name AS student, s.group AS groupName 
ORDER BY student 
LIMIT 10;

Задание 4. Запросы по связям (Одношаговый и Двухшаговый)
// Одношаговый переход: Студенты и их курсы
MATCH (s:Student)-[:STUDIES]->(c:Course) 
RETURN s.name AS student, c.title AS course;

// Цепочка из двух отношений: Преподаватель -> Курс <- Студент
MATCH (t:Teacher)-[:TEACHES]->(c:Course)<-[:STUDIES]-(s:Student) 
RETURN t.name AS teacher, c.title AS course, s.name AS student;
Пояснение шаблона: Шаблон (t:Teacher)-[:TEACHES]->(c:Course)<-[:STUDIES]-(s:Student) связывает преподавателя t с курсом c, который одновременно изучает студент s. Направление стрелок показывает входящие и исходящие связи относительно узла Course.

Задание 5. Фильтрация данных с помощью WHERE
// Фильтр по строковому свойству (Группа)
MATCH (s:Student) 
WHERE s.group = "IS-24-1" 
RETURN s.name, s.group;

// Фильтр по числовому свойству (Кредиты >= 5)
MATCH (c:Course) 
WHERE c.credits >= 5 
RETURN c.title, c.credits;

Задание 6. Модификация свойств (SET)
// Изменение свойства курса/студента
MATCH (s:Student {id: 1}) 
SET s.year = 4 
RETURN s;

// Добавление свойства к отношению (номер семестра)
MATCH (s:Student {id: 1})-[r:STUDIES]->(c:Course {id: 101}) 
SET r.semester = 5 
RETURN s.name, r.semester, c.title;

Задание 7. Безопасное создание и удаление узла (DETACH DELETE)
// Создание временного тестового узла
CREATE (:Temp {id: 999, note: "delete-me"});

// Удаление узла (с возможными связями через DETACH DELETE)
MATCH (n:Temp {id: 999}) 
DETACH DELETE n;

// Проверка успешного удаления (должно вернуть 0)
MATCH (n:Temp {id: 999}) 
RETURN count(n) AS remaining;

Задание 8. Повторный запуск MERGE и проверка на дубликаты
// Повторный запуск операции MERGE для существующего узла
MERGE (s1:Student {id: 1}) SET s1.name = "Aibek", s1.group = "IS-24-1", s1.year = 4;

// Проверка общего количества студентов (должно остаться ровно 4)
MATCH (s:Student) 
RETURN count(s) AS totalStudents;
Пояснение: Команда CREATE всегда создает новый узел, что при повторном запуске скрипта привело бы к появлению дубликатов. Команда MERGE сначала выполняет поиск узла по заданному шаблону/ИД. Если узел найден — он не пересоздается, а лишь обновляются его свойства с помощью SET. Наличие CREATE CONSTRAINT гарантирует уникальность поля id на уровне базы данных.

Задание 7 (Дополнительное). Поиск общих соседей
// Поиск пар студентов, изучающих одни и те же дисциплины
MATCH (a:Student)-[:STUDIES]->(c:Course)<-[:STUDIES]-(b:Student) 
WHERE a.id < b.id 
RETURN a.name AS firstStudent, b.name AS secondStudent, collect(DISTINCT c.title) AS sharedCourses;

5. Ответы на контрольные вопросы
Что такое property graph?

Это граф, в котором сущности представлены узлами (Nodes), связи между ними — отношениями (Relationships), а детализирующие данные хранятся в виде пар «ключ-значение» (Properties) у узлов и отношений.

Чем узел отличается от отношения?

Узел представляет самостоятельный объект (сущность), а отношение указывает на наличие и смысл связи между двумя конкретными узлами.

Какую роль выполняют метки и свойства?

Метки (Labels) группируют узлы по типам (типизируют сущности), а свойства (Properties) содержат атрибутивный состав (характеристики) этих узлов или связей.

Что означает направление связи?

Оно определяет смысловую направленность действия (например, Студент изучаeт Курс, а не наоборот).

Для чего используются CREATE и MERGE?

CREATE создает элементы безусловно (с рисками дублирования), а MERGE работает по принципу «найти или создать».

Как работает MATCH?

Ищет в графе подграфы, соответствующие заданному визуальному шаблону (шаблону сопоставления).

Чем WHERE отличается от RETURN?

WHERE фильтрует выборку по условиям, а RETURN указывает, какие конкретно поля/узлы должны попасть в итоговый отклик.

Как получить связанные узлы за два перехода?

Задав цепочку сопоставления с промежуточным узлом: MATCH (a)-[:REL1]->(b)-[:REL2]->(c) RETURN a, c.

Для чего нужны ORDER BY и LIMIT?

ORDER BY осуществляет сортировку выводимого результата, а LIMIT ограничение размера результирующего списка.

Как изменить свойства узла и отношения?

Путем сопоставления элемента в MATCH и последующего применения инструкции SET n.prop = value.

Чем DELETE отличается от DETACH DELETE?

Обычный DELETE выдаст ошибку, если у узла есть хотя бы одна связь. DETACH DELETE предварительно удаляет все инцидентные связи, после чего удаляет сам узел.

Зачем создавать ограничения уникальности?

Чтобы предотвратить создание дубликатов с одинаковыми идентификаторами и автоматически ускорить поиск через создание внутренних индексов.

Как проверить отсутствие дубликатов?

Сравнить общее количество элементов через count(n) с количеством уникальных значений полей через count(DISTINCT n.id).

Когда графовая модель предпочтительнее табличной?

В задачах с высокой связностью данных (социальные сети, рекомендации, логистика), где реляционные JOIN работают медленно, а графовый обход выполняется за константное время благодаря указателям смежности.

6. Вывод
В ходе лабораторной работы были освоены базовые принципы работы с графовой СУБД Neo4j и языком Cypher. В процессе выполнения заданий создана учебная база данных предметной области «Университет», содержащая 12 узлов и 16 направленных отношений. Были успешно реализованы механизмы обеспечения целостности данных (CREATE CONSTRAINT, MERGE), сложные сопоставления графовых шаблонов, включая двухшаговые запросы и поиск общих соседей (collect, DISTINCT), а также операции безопасного модифицирования и удаления элементов (SET, DETACH DELETE). Графовая модель продемонстрировала высокую наглядность и удобство при анализе многомерных связей между сущностями.
